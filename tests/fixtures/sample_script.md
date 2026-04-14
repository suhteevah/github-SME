# GitHub Actions: Building Your First CI Pipeline

## Scene 1: Introduction
**Visual:** Presenter at desk, GitHub Actions logo on screen
**Voiceover:** Every time you push code to GitHub, you're making a bet — a bet that your changes work. GitHub Actions lets you automate the verification of that bet.

## Scene 2: What is CI?
**Visual:** Diagram showing code push → build → test → deploy
**Voiceover:** Continuous Integration means automatically building and testing your code every time someone pushes a change. Instead of finding out something is broken at 3 AM on deploy day, you find out in minutes.

## Scene 3: Creating Your First Workflow
**Visual:** Screen recording of VS Code with .github/workflows directory
**Voiceover:** Let's create our first workflow. In your repository, create a directory called `.github/workflows`. Inside it, create a file called `ci.yml`.

**On screen — code:**
```yaml
name: CI Pipeline
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
```

## Scene 4: Understanding the Workflow
**Visual:** Annotated YAML with arrows pointing to each section
**Voiceover:** Let's break this down. The `on` section tells GitHub when to run this workflow — on pushes to main and on pull requests. The `jobs` section defines what to do. We're running on Ubuntu, checking out our code, setting up Node.js version 18, installing dependencies, and running tests.

## Scene 5: Viewing Results
**Visual:** Screen recording of GitHub Actions tab showing green checkmark
**Voiceover:** After pushing this file, go to the Actions tab in your repository. You'll see your workflow running. A green checkmark means everything passed. A red X means something failed — and GitHub will show you exactly what went wrong.

## Scene 6: Adding Matrix Testing
**Visual:** Updated YAML file
**Voiceover:** What if you want to test against multiple Node versions? GitHub Actions supports matrix strategies. Let's update our workflow:

**On screen — code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm install
      - run: npm test
```

**Voiceover:** Now GitHub will run your tests three times in parallel — once for each Node version. This is how professional teams ensure compatibility across environments.
