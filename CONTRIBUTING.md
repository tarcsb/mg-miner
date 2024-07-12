# Contributing to mg-miner

Thank you for considering contributing to `mg-miner`! Your contributions are highly valued. Please take a moment to review this guide to ensure a smooth contribution process.

## Getting Started

1. **Fork the Repository**: Click on the "Fork" button on the top right of the repository page to create a copy of the repository in your GitHub account.

2. **Clone Your Fork**: Clone your fork to your local machine using the following command:

    ```sh
    git clone https://github.com/your-username/mg-miner.git
    cd mg-miner
    ```

3. **Create a Branch**: Create a new branch for your feature or bug fix:

    ```sh
    git checkout -b my-feature-branch
    ```

4. **Set Up Environment**: Create a virtual environment and install dependencies:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Making Changes

1. **Update Configuration**: If your changes require updates to the configuration file, ensure these changes are documented and tested.

2. **Add Tests**: Add tests for your new feature or bug fix. This helps ensure that your changes do not break existing functionality and that your code works as expected.

3. **Run Tests**: Run the tests to ensure all tests pass:

    ```sh
    python -m unittest discover tests
    ```

4. **Document Changes**: Update the documentation to reflect your changes. This includes the `README.md`, configuration examples, and any relevant comments in the code.

## Committing Changes

1. **Commit Your Changes**: Commit your changes with a clear and concise commit message:

    ```sh
    git add .
    git commit -m "Add feature X to improve Y"
    ```

2. **Push to Your Fork**: Push your changes to your forked repository:

    ```sh
    git push origin my-feature-branch
    ```

## Submitting a Pull Request

1. **Open a Pull Request**: Navigate to the original repository and click on the "New Pull Request" button. Choose your fork and branch as the source and the main repository's branch as the destination.

2. **Describe Your Changes**: Provide a clear and detailed description of your changes in the pull request. Include any relevant issue numbers if your pull request addresses an existing issue.

3. **Submit Your Pull Request**: Submit the pull request and wait for the maintainers to review your changes. Be responsive to any feedback and make necessary updates.

## Code of Conduct

Please adhere to the project's code of conduct in all your interactions with the community. Respectful and constructive communication is expected.

## Contact

If you have any questions or need further assistance, feel free to contact Jeffrey Plewak at plewak.jeff@gmail.com.

Thank you for your contributions!

© 2024 Jeffrey Plewak. All Rights Reserved.
