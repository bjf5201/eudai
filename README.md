<!-- markdownlint-disable MD033-->
<h1 align="center">ShellGPT</h1>
<p align="center">Lightweight, privacy-focused GPT for your shell.</p>

<pre align="center">
  <code>pnpm i -g shellgpt</code>
</pre>

## Overview

## Requirements

## Installation

## Developer Instructions

## Using Projects for Organization

1. Add your first project

    ```shell
    shellgpt project create <project-title>
    ```

    This will initialize a new project named `portfolio`:

    ```shell
    shellgpt project create portfolio
    ```

    Options:
    - `-d, --description <text>`: Multi-line description
    - `-s, --status <status_type>`: Defaults to "backlog"
    - `-l, --label <label1>,[label2]`: Must have at least one label, but can include multiple labels separated by a comma

2. Upload context to the project (via a filepath or a URL)

    For a file:

    ```shell
    shellgpt project upload [-f|--file] <filepath>
    ```

    For a website URL:

    ```shell
    shellgpt project upload [-u|--url] <url>
    ```

3. Start a new conversation

    ```shell
    shellgpt convo start [convo-name]
    ```

    Options:
    - `-l, --label <label1>,<label2>`: Must include at least one label with this option, but can add as many labels as necessary
    - `-d, --description <description-text>`: Multi-line description
    - `-p, --project <project-name`: Add this conversation to a specific project

4. Start a new conversation within a project

    ```shell
    shellgpt convo create [-p|--project] <project-name>
    ```
