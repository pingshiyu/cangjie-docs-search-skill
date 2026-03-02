# Central Repository Artifact Specification

The central repository manages third-party libraries in the form of **artifacts**. The following are important concepts regarding artifacts:

*   **Artifact Package**: A source code archive, representing the smallest unit for storing a third-party library in the central repository. An artifact package has the following three key attributes:
    *   **Artifact Name**: The name used to label the artifact package.
    *   **Artifact Version**: The version number used to label the artifact package.
    *   **Organization Name** (optional): The name used to label the organization to which the artifact package belongs. An artifact package may not belong to any organization.
*   **Artifact**: The collection of all artifact package versions that share the same artifact name and organization name.
*   **Organization**: A collaborative group that develops and maintains one or more artifacts. Artifact names must be unique within the same organization or among artifacts without an organization.

> **Note:**
>
> *   Artifact names and organization names consist of uppercase letters, lowercase letters, numbers, and underscores. Their length must be between 3 and 64 characters inclusive. They must start with a letter or one or more underscores. If starting with an underscore, the first non-underscore character must be a letter. For example: `cangjie_demo_1`, `__Cangjie_Demo_2`.
> *   Artifact names and organization names cannot be any keyword from the Cangjie syntax (case-insensitive), and an organization name cannot be `default`.
> *   The artifact version number format is `Major.Minor.Patch`. All three level numbers are natural numbers. For example: `0.1.2`, `123.456.789`.