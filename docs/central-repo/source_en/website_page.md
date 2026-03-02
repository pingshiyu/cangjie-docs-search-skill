# Central Repository Website

The [Central Repository Website](https://pkg.cangjie-lang.cn) is the front-end web page for the central repository, providing account operations, artifact search, organization management, and other functionalities.

## Registering an Account

The "Login" button in the top-right corner of the website is used to register a central repository account or to log in to an existing account.

If a user is logged into a GitCode account, they can directly authenticate and log in to the central repository. In addition to GitCode, the central repository also supports login via the methods listed under "Other Login Methods" in the login page.

## Personal Information

After logging in, the username and avatar can be seen in the top-right corner of the website. Clicking on the username or avatar leads to the personal homepage, where users can view their personal information, uploaded artifacts, and follow lists.

![Homepage](../figures/user-home.png)

Moving the cursor over the username or avatar reveals a dropdown menu. From here, users can access the personal center page to view or modify personal information, or to see a list of organizations they have created or joined.

![Personal Center](../figures/user-center.png)

Furthermore, on the personal center page, users can perform user token-related operations, including creating, refreshing, and deleting tokens. The obtained user token is used for the central repository client's [Repository Configuration](./client/config.md#repository-configuration).

![Token](../figures/token.png)

## Artifact Information

Entering an artifact name in the search box at the top of the central repository page allows users to search for artifacts within the repository. Pressing `Shift + S` or `/` quickly focuses the search box. The search box can also be used to search for organizations.
Currently, the search function only supports prefix search.

![Search](../figures/search.png)

Clicking on an artifact entry leads to the artifact details page, where information about the artifact can be viewed, including the `README`, author, tags, artifact homepage, etc.

![Artifact Page](../figures/artifact.png)

## Organization Management

On the organization page within the personal center, users can apply to create an organization. Naming conventions for organization names are detailed in the [Central Repository Artifact Specification](./artifact.md). If an organization name involves well-known enterprises, users must also provide proof via the DNS TXT Record of the enterprise domain name; otherwise, the application will not be approved. Organization names that do not comply with laws and regulations will also not be approved.

![Create Organization](../figures/create-org.png)

After creating an organization, the creator becomes the **administrator** of the organization by default. Each organization has one and only one administrator. The administrator can access the corresponding organization's management page via the organization page in the personal center to manage the organization, including operations such as inviting members, removing members, and transferring administrator rights.

![Manage Organization](../figures/manage-org.png)

Organizations and artifacts within organizations can also be searched via the search box.