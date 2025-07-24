# Evo AI Agent

Temporary repository for developing an ADK-flavored Evo AI agent.

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Read access to the labs-pypi-virtual repository in [JFrog Artifactory](https://seequent.jfrog.io/ui/repos/tree/General/labs-pypi-virtual?projectKey=labs)
- gcloud cli installed and configured 
  - [gcloud sdk installation](https://cloud.google.com/sdk/docs/install)


### Python Repository Authentication

Follow the [instructions to setup HTTP authentication](https://docs.astral.sh/uv/configuration/authentication/#http-authentication) for JFrog Artifactory in your environment. The simplest options seems to be a `.netrc` configuration file.

If using a `.netrc` configuration file, start by [generating an identity token](https://jfrog.com/help/r/jfrog-platform-administration-documentation/generate-identity-token) in the Artifactory UI. Then add the following line to your `.netrc` file:

```sh
machine seequent.jfrog.io login <username>@bentley.com password <identity_token>
```

Where `<username>` is your Bentley email address, and `<identity_token>` is the identity token you generated.

### Installing the project

`uv` manages the python environment and dependencies for the project. To install the project, run the following command in the root directory of the project:

```sh
uv sync
```

## Testing the agent with ADK

In the root directory, run the following command to test the Evo AI agent:

```sh
uv run adk web src
```

The ADK evaluation server will start, and you can access the agent at `http://localhost:8000/dev-ui/?app=evo_ai`. The default vscode launch configuration will also start the ADK evaluation server for you.
