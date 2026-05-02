# CPE494-erp-invoice-app-by-ai

This repository contains an **ASP.NET Core ERP Invoice application** generated and iteratively developed by a **multi-agent AI coding team**.

Companion repository: **CPE494-agent-coding-team**

## Objective

This project demonstrates how AI agents can collaborate to build a real-world software system across multiple development sprints.

It is part of the **CPE494 course**, where students learn how to:

- Use AI agents as a software engineering team
- Review and validate AI-generated code
- Manage agent-generated code in Git
- Build an enterprise-style ERP module using ASP.NET Core

## How This App Is Built

This application is produced by a coordinated set of AI agents:

- **Architect**: plans structure and tasks
- **Coder**: generates source code
- **Logic Tester**: validates correctness and data integrity
- **UI Auditor**: checks UI/UX rules and design consistency

A human developer remains in the loop to review plans, approve changes, verify build results, and manage version control.

## Planned Sprints

- **Sprint 1**: App shell, layout, Zen Green theme, landing page
- **Sprint 2**: Authentication and authorization
- **Sprint 3**: Product and customer management
- **Sprint 4**: Invoice processing with header and line items
- **Sprint 5**: Reporting, validation, UI polish, and final review

## Technology Stack

- **Backend**: ASP.NET Core Razor Pages, C#
- **Database**: Entity Framework Core
- **Frontend**: CSS, Tabulator, Font Awesome
- **Theme**: Zen Green
- **Version Control**: Git and GitHub

## Project Structure

```text
Pages/          Razor Pages UI
Models/         Data models
Data/           Database context and configuration
wwwroot/        Static assets such as CSS, JavaScript, and icons
```

## Quick Start

```bash
dotnet build
dotnet run
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:5000
```

## Notes for Students

This repository represents the output of an AI-driven development process.

Do not assume AI-generated code is correct by default. Your job is to inspect, test, validate, and improve the generated application.

## Key Idea

AI can act as a structured development team, but only when guided, constrained, and reviewed properly.

## License

For educational use in CPE494.
