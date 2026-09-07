"""公式解析、依赖排序及代码恢复，不执行导入文件。"""

import ast
import builtins
import keyword
import re
from dataclasses import dataclass
from .helpers import SYMPY_NAMES, tr


def normalize(expression):
    return re.sub(r"\blambda\b", "lamda", expression.replace("^", "**"))


def loaded_names(expression):
    tree = ast.parse(expression, mode="eval")
    local = {
        n.id
        for n in ast.walk(tree)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)
    }
    local.update(n.arg for n in ast.walk(tree) if isinstance(n, ast.arg))
    return {
        n.id
        for n in ast.walk(tree)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
    } - local


@dataclass
class FormulaPlan:
    symbols: list
    intermediates: list
    expressions: list
    analysis_symbols: list

    def source(self):
        from . import helpers as h

        blocks = []
        if self.symbols:
            names = ", ".join(self.symbols)
            blocks.append(
                h.code_comment("symbols")
                + "\n"
                + names
                + " = symbols("
                + repr(names)
                + ")"
            )
        if self.intermediates:
            blocks.append(
                h.code_comment("intermediates")
                + "\n"
                + "\n".join(name + " = " + expr for name, expr in self.intermediates)
            )
        blocks.append(
            h.code_comment("expressions")
            + "\nexpressions = {\n"
            + "".join(
                "    " + repr(name) + ": " + expr + ",\n"
                for name, expr in self.expressions
            )
            + "}"
        )
        return "\n\n".join(blocks)


def formula_error(message, line):
    exc = ValueError(tr("line_error", line=line, message=message))
    exc.lineno = line
    return exc


def parse_formulas(text):
    items, plots = [], []
    reserved = set(SYMPY_NAMES) | set(dir(builtins)) | {"np", "numpy"}
    for line, raw in enumerate(text.splitlines(), 1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        if ":=" in raw:
            name, expression = raw.split(":=", 1)
            name = normalize(name.strip())
            if (
                not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", name)
                or keyword.iskeyword(name)
                or name in reserved
            ):
                raise formula_error(tr("invalid_name", name=name), line)
            expression = normalize(expression.strip())
            try:
                refs = loaded_names(expression)
            except SyntaxError as exc:
                raise formula_error(exc.msg, line) from None
            items.append((name, expression, refs))
        elif "=" in raw:
            name, expression = raw.split("=", 1)
            name, expression = name.strip(), normalize(expression.strip())
            if not name or not expression:
                raise formula_error(tr("invalid_line", line=line), line)
            if name in [p[0] for p in plots]:
                raise formula_error(tr("duplicate_label", name=name), line)
            try:
                loaded_names(expression)
            except SyntaxError as exc:
                raise formula_error(exc.msg, line) from None
            plots.append((name, expression))
        else:
            raise formula_error(tr("invalid_line", line=line), line)
    if not plots:
        raise ValueError(tr("empty_formula"))
    indices = {}
    for i, (name, _, _) in enumerate(items):
        indices.setdefault(name, []).append(i)
    dependencies = []
    for i, (name, expr, refs) in enumerate(items):
        deps = set()
        for ref in refs & indices.keys():
            previous = [j for j in indices[ref] if j < i]
            target = previous[-1] if previous else indices[ref][0]
            deps.add(target)
        # Reassignments must preserve their original order, even without self-reference.
        previous = [j for j in indices[name] if j < i]
        if previous:
            deps.add(previous[-1])
        dependencies.append(deps)
    order, pending = [], set(range(len(items)))
    while pending:
        ready = [i for i in sorted(pending) if dependencies[i] <= set(order)]
        if not ready:
            raise ValueError(
                tr("cycle", names=", ".join(items[i][0] for i in sorted(pending)))
            )
        order.extend(ready)
        pending.difference_update(ready)
    all_refs = set().union(
        *(refs for _, _, refs in items), *(loaded_names(expr) for _, expr in plots)
    )
    labels = {name for name, _ in plots}
    conflict = (all_refs & labels) - indices.keys() - reserved
    if conflict:
        raise ValueError(tr("label_ref", name=", ".join(sorted(conflict))))
    symbols = sorted(all_refs - indices.keys() - labels - reserved)
    ordered = [(items[i][0], items[i][1]) for i in order]
    dependencies = {}
    for name, expression in ordered:
        dependencies[name] = free_names(
            ast.parse(expression, mode="eval").body, dependencies
        )
    available = set().union(
        *(
            free_names(ast.parse(expr, mode="eval").body, dependencies)
            for _, expr in plots
        )
    )
    return FormulaPlan(symbols, ordered, plots, sorted(available & set(symbols)))


def free_names(node, intermediates):
    """查找表达式的自由参数，保留积分上下限中的外部变量。"""
    if isinstance(node, ast.Name):
        return set(intermediates.get(node.id, {node.id}))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        if (
            name in ("integrate", "Integral", "summation", "Sum", "product", "Product")
            and node.args
        ):
            result = free_names(node.args[0], intermediates)
            for limit in node.args[1:]:
                if isinstance(limit, (ast.Tuple, ast.List)) and len(limit.elts) == 3:
                    result -= free_names(limit.elts[0], intermediates)
                    for bound in limit.elts[1:]:
                        result |= free_names(bound, intermediates)
                else:
                    result |= free_names(limit, intermediates)
            for kw in node.keywords:
                result |= free_names(kw.value, intermediates)
            return result
        if name == "limit" and len(node.args) >= 3:
            return (
                free_names(node.args[0], intermediates)
                - free_names(node.args[1], intermediates)
            ) | free_names(node.args[2], intermediates)
    if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
        scope = dict(intermediates)
        result = set()
        for generator in node.generators:
            result |= free_names(generator.iter, scope)
            for target in ast.walk(generator.target):
                if isinstance(target, ast.Name):
                    scope[target.id] = set()
            for condition in generator.ifs:
                result |= free_names(condition, scope)
        for value in (
            [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
        ):
            result |= free_names(value, scope)
        return result
    return set().union(
        *(free_names(child, intermediates) for child in ast.iter_child_nodes(node))
    )


def parse_assignments(text):
    raw = text.strip()
    if not raw:
        return {}
    if raw.startswith("{"):
        result = literal(ast.parse(raw, mode="eval").body, {})
    else:
        raw = ",".join(
            line.strip().rstrip(",") for line in raw.splitlines() if line.strip()
        )
        call = ast.parse("dict(" + raw + ")", mode="eval").body
        if call.args or any(kw.arg is None for kw in call.keywords):
            raise ValueError(tr("invalid_assignments"))
        result = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
    if not isinstance(result, dict) or any(
        not isinstance(name, str) or not name.isidentifier() for name in result
    ):
        raise ValueError(tr("invalid_assignments"))
    return result


class AssignmentMemory:
    """每个标签页独立保留参数最近一次的固定赋值。"""

    def __init__(self):
        self.values = {}

    def remember(self, text):
        self.values.update(parse_assignments(text))

    def text(self, symbols, axes):
        names = [name for name in symbols if name not in axes]
        for name in names:
            self.values.setdefault(name, 1.0)
        return ", ".join(name + "=" + repr(self.values[name]) for name in names)


def literal(node, values):
    if isinstance(node, ast.Name):
        return values.get(node.id, node.id)
    if isinstance(node, (ast.List, ast.Tuple)):
        result = [literal(n, values) for n in node.elts]
        return tuple(result) if isinstance(node, ast.Tuple) else result
    if isinstance(node, ast.Dict):
        return {
            literal(k, values): literal(v, values)
            for k, v in zip(node.keys, node.values)
        }
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "dict"
        and not node.args
    ):
        return {kw.arg: literal(kw.value, values) for kw in node.keywords if kw.arg}
    return ast.literal_eval(node)


def read_plot_code(code):
    from .helpers import PLOT_FUNCTIONS, SAVE_FINAL_CODE

    tree = ast.parse(code)
    values, nodes, call, call_node = {}, {}, None, None
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if (
                isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id in PLOT_FUNCTIONS
            ):
                call, call_node = node.value, node
                break
            nodes.setdefault(name, []).append(node)
            try:
                values[name] = literal(node.value, values)
            except (ValueError, TypeError):
                pass
    if call is None:
        raise ValueError(tr("unsupported_code"))
    function = call.func.id
    import inspect
    import betu as core_functions
    from .table import plot_table

    fn = plot_table if function == "plot_table" else getattr(core_functions, function)
    parameters = dict(values)
    for key, node in zip(inspect.signature(fn).parameters, call.args):
        parameters[key] = literal(node, values)
    for kw in call.keywords:
        if kw.arg:
            parameters[kw.arg] = literal(kw.value, values)
        else:
            parameters.update(literal(kw.value, values))
    formula = ""
    if function != "plot_table":
        expression_node = nodes.get("expressions", [None])[-1]
        if expression_node is None or not isinstance(expression_node.value, ast.Dict):
            raise ValueError(tr("unsupported_code"))
        expressions = [
            (ast.literal_eval(k), ast.get_source_segment(code, v))
            for k, v in zip(expression_node.value.keys, expression_node.value.values)
        ]
        refs = set().union(*(loaded_names(expr) for _, expr in expressions))
        intermediate_names = set()
        excluded = set(inspect.signature(fn).parameters) | {
            "expressions",
            "assigns",
            "legend_options",
        }
        changed = True
        while changed:
            changed = False
            for name in refs & nodes.keys() - excluded - intermediate_names:
                # symbols() declarations remain symbols, not intermediate assignments.
                if any(
                    isinstance(n.value, ast.Call)
                    and isinstance(n.value.func, ast.Name)
                    and n.value.func.id in ("symbols", "Symbol")
                    for n in nodes[name]
                ):
                    continue
                intermediate_names.add(name)
                for n in nodes[name]:
                    refs.update(loaded_names(ast.get_source_segment(code, n.value)))
                changed = True
        lines = []
        for node in tree.body:
            if (
                isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in intermediate_names
            ):
                lines.append(
                    node.targets[0].id
                    + " := "
                    + ast.get_source_segment(code, node.value)
                )
        lines.extend(name + " = " + expr for name, expr in expressions)
        formula = "\n".join(lines)
    after = code.splitlines()[call_node.end_lineno :]
    advanced = []
    for node in tree.body:
        if node.lineno <= call_node.end_lineno:
            continue
        if ast.dump(node) == ast.dump(ast.parse(SAVE_FINAL_CODE).body[0]):
            continue
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "title"
            and len(node.body) == 1
        ):
            statement = node.body[0]
            if (
                isinstance(statement, ast.Expr)
                and isinstance(statement.value, ast.Call)
                and isinstance(statement.value.func, ast.Attribute)
                and statement.value.func.attr == "title"
                and statement.value.args
                and isinstance(statement.value.args[0], ast.Name)
                and statement.value.args[0].id == "title"
            ):
                continue
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "plot_context"
        ):
            continue
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == "show"
        ):
            continue
        advanced.append(ast.get_source_segment(code, node))
    return function, formula, parameters, "\n".join(advanced)
