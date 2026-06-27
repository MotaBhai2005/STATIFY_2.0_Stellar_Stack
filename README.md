# STATIFY_2.0_Stellar-Stack

## GenAI Financial Analyst Chatbot
🚧 Project Status: Under Development

This repository contains our submission for the STATIFY 2.0 – Week 1: Financial Analyst Chatbot project.

The project is currently under active development by our team. We are implementing an AI-powered financial assistant capable of providing real-time stock prices and the latest market news using a Hugging Face LLM, LangChain, and external tools.

The complete source code, documentation, setup instructions, and all required project files will be uploaded to this repository upon completion.

Expected Deployment: **Before 6:00 PM (IST), Sunday**.

Thank you for your patience.





An LLM-powered financial assistant designed to retrieve real-time stock prices and aggregate recent market news to provide comprehensive, live market insights. This project utilizes open-source models from Hugging Face alongside tool calling/agentic reasoning to dynamically fetch financial data and browse the web.

---

## 🤝 Git Workflow & Repository Code of Conduct

To maintain code stability and ensure high quality, all team members must follow this development workflow:

### 🚫 1. Never Commit Directly to `main`
The `main` branch acts as the production-ready source of truth. Direct commits or pushes to `main` are strictly prohibited. All changes must go through a feature branch and a pull request (PR).

### 🌿 2. Branching Strategy
When starting work on a new feature, bug fix, or task:
1. Ensure your local `main` is up to date:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Create and switch to a new descriptive feature branch:
   ```bash
   git checkout -b <type>/<short-description>
   ```
   * *Examples:*
     * `feature/yfinance-integration`
     * `bugfix/fix-news-parser`
     * `docs/update-readme-guidelines`

### 🍴 3. Forking Workflow (Optional/External)
If you are collaborating across separate user profiles:
1. Fork this repository on GitHub.
2. Clone your fork locally, make changes, and push them to your fork.
3. Submit a Pull Request from your fork's feature branch to this repository's `main` branch.

### 🔍 4. Commit and Pull Request (PR) Guidelines
* **Commit Messages:** Keep commit messages concise and descriptive (e.g., `git commit -m "feat: add schema validation for stock output"`).
* **Open a Pull Request:** Once your work on the feature branch is complete and pushed to GitHub, open a PR targeting the `main` branch.
* **Review Process:** 
  * At least one other team member should review the code before merging.
  * Ensure the chatbot builds and runs locally without errors before requesting a merge.

---

## 📊 Evaluation Criteria Met
* **Functionality & Accuracy:** Integrates real-time financial APIs and web-scraping to answer financial queries with ground-truth data.
* **Tool Integration:** Uses LangChain's tool bindings to seamlessly route queries between the LLM and external data sources.
* **Code Quality:** Well-defined files, separation of concerns, and rigorous validation via Pydantic.
