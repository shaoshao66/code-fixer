
if [ -z "$(docker images -q codefixer/code-fixer 2> /dev/null)" ]; then
  echo "⚠️ Please wait for the postCreateCommand to start and finish (a new window will appear shortly) ⚠️"
fi

echo "Here's an example Code-Fixer command to try out:"

echo "codefixer run \\
  --agent.model.name=claude-sonnet-4-20250514 \\
  --agent.model.per_instance_cost_limit=2.00 \\
  --env.repo.github_url=https://github.com/SWE-agent/test-repo \\
  --problem_statement.github_url=https://github.com/SWE-agent/test-repo/issues/1 \\
"
