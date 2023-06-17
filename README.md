# depwatch

depwatch is a simple command-line tool for collecting the times of various events in your project's lifecycle, from code commits to deployments. Event times are retrieved from repository management tools (like GitHub) and CI tools (like CircleCI).

## Installation

Install depwatch using pip:

```shell-session
$ pip install depwatch
```

## Usage

Execute the command with your access tokens.

```shell-session
GITHUB_ACCESS_TOKEN=<your_token> CIRCLECI_ACCESS_TOKEN=<your_token> depwatch <user_name>/<repository_name>
```

The results are output to the output.csv file.

```shell-session
$ cat output.csv
first_committed_at,merged_at,deployed_at
2023-02-25T00:48:18+00:00,2023-02-25T00:57:06+00:00,2023-02-25T00:58:11+00:00
2023-02-25T00:46:52+00:00,2023-02-25T00:54:05+00:00,2023-02-25T00:55:12+00:00
2023-02-25T00:43:47+00:00,2023-02-25T00:45:33+00:00,2023-02-25T00:46:39+00:00
...
```

### Note: Using the `.env` file

Alternatively, you can use the `.env` file. Create the `.env` file in the directory where you want to run the command as follows.

```shell-session
cp .env.example .env
```

Set the values according to the instructions in the `.env` file.

### Note: Scope of the GitHub Personal Access Token

GitHub offers [two types of personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), fine-grained personal access tokens and classic personal access tokens. For personal repositories, you can use both. For organizatio repositories, we recommend using classic tokens, as we know that fine-grained tokens do not allow you to get private repositories.

If you use fine-grained personal access tokens, specify read-only permissions for **Contents**, **Metadata**, and **Pull requests**. If you use classic personal access tokens, specify **repo** scope.

### Options

```shell-session
# get the latest 10 items (default is `100`)
depwatch your_name/your_project --limit 10

# get the item of PRs created from January 1, 2023, to March 31, 2023
depwatch your_name/your_project --created-at 2023-01-01..2023-03-31

# get only the data of PRs (do not get the data of CI)
depwatch your_name/your_project --code-only

# get by specifying the deployment workflow name of CI
depwatch your_name/your_project -workflow-name deploy-to-production
```

## Contributing

Comming soon!

- TODO: Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## License

This code is released under the MIT License. See [LICENSE](/LICENSE) for details.
