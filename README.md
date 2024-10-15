# Cloud Infrastructure Designer and Critique System

This project leverages two OpenAI-powered agents to provide Cloud Infrastructure implementation guidance and critical feedback. The system consists of:

1. **Cloud Infrastructure Expert** - The first agent generates detailed cloud infrastructure implementation instructions based on the user's prompt.
2. **Technical Critic** - The second agent reviews and provides a technical critique of the implementation produced by the first agent.

The final output of this system is the critique of the implementation instructions.

## Table of Contents

- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Prompt File Format](#prompt-file-format)
- [Contributing](#contributing)
- [License](#license)

## How It Works

1. The user provides a prompt file containing the necessary details about the desired cloud infrastructure setup.
2. The **Cloud Infrastructure Expert** agent generates a set of implementation instructions based on the prompt.
3. The **Technical Critic** agent analyzes the generated instructions and provides a critique, pointing out any potential issues, optimizations, or improvements.
4. The output is the technical critique of the implementation
