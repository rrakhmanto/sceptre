import click

from sceptre.context import SceptreContext
from sceptre.cli.helpers import catch_exceptions, get_stack_or_stack_group
from sceptre.plan.plan import SceptrePlan


@click.command(name="set-policy")
@click.argument("path")
@click.argument("policy-file", required=False)
@click.option(
    "-b", "--built-in", type=click.Choice(["deny-all", "allow-all"]),
    help="Specify a built in stack policy."
)
@click.pass_context
@catch_exceptions
def set_policy_command(ctx, path, policy_file, built_in):
    """
    Sets stack policy.

    Sets a specific stack policy for either a file or using a built-in policy.
    """
    context = SceptreContext(
                command_path=path,
                project_path=ctx.obj.get("project_path"),
                user_variables=ctx.obj.get("user_variables"),
                options=ctx.obj.get("options")
            )

    stack, _ = get_stack_or_stack_group(context)

    if built_in == 'deny-all':
        action = 'lock'
        plan = SceptrePlan(context, action, stack)
        plan.execute()
    elif built_in == 'allow-all':
        action = 'unlock'
        plan = SceptrePlan(context, action, stack)
        plan.execute()
    else:
        action = 'set_policy'
        plan = SceptrePlan(context, action, stack)
        plan.execute(policy_file)
