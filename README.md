# GitHub Candidate Profiler

## Overview
GitHub Candidate Profiler is a web application designed to help employers search for potential candidates on GitHub. The application allows users to view candidate profiles, save potential candidates, and manage a list of saved candidates. It leverages the GitHub API to fetch candidate information and provides an intuitive interface for employers to review and manage candidates.

## Features
- **Candidate Search**: View detailed information about GitHub users, including their name, username, location, avatar, email, profile URL, and company.
- **Save Candidates**: Save potential candidates to a list for future reference.
- **Skip Candidates**: Skip candidates that are not suitable.
- **Saved Candidates List**: View a list of previously saved candidates with their details.
- **Persistent Storage**: Saved candidates are stored locally and persist across page reloads.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/github-candidate-profiler.git
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your GitHub token to the `.env` file:
     ```
     GITHUB_TOKEN=your-github-token
     ```

4. Run the development server:
    ```bash
    npm run dev
    ```

## Usage
### Navigate to the Candidate Search page:
- The application will automatically fetch and display a candidate's information.
- Use the "+" button to save a candidate to the list of potential candidates.
- Use the "-" button to skip a candidate and view the next one.

### View Saved Candidates:
- Navigate to the Saved Candidates page to view a list of saved candidates.
- The list will persist across page reloads.

## Project Structure
```plaintext
src
│
├── api/                # Contains API functions for fetching candidate data from GitHub.
├── components/         # Contains reusable React components.
├── interfaces/         # Contains TypeScript interfaces.
├── pages/              # Contains page components for different routes.
│
├── App.tsx             # Main application component.
├── main.tsx            # Entry point of the application.
└── index.css           # Global styles.
