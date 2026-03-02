# Central Repository Communication Specification

Using `repository.home.registry` configured by the user in `cangjie-repo.toml` as the base, `cjpm` will send upload and download requests for artifacts and indices to the central repository according to the communication specification defined in this chapter.

## Artifact Package Upload

`cjpm publish` publishes the artifact package and metadata corresponding to the `cjpm` module packaged by `bundle` to the central repository. The corresponding `API` specification is:

*   **Method**: `POST`
*   **`url`**:
    *   Module without organization: `/pkg/${module-name}`
    *   Module within an organization: `/pkg/${module-name}?organization=${org-name}`
*   **`header`**:
    *   User token: `Authorization=${token}`
*   **`body`**:
    *   Metadata:
        *   Metadata version (1 byte), corresponding to `meta-version` in the metadata.
        *   Metadata length (4 bytes), corresponding to the byte length *m* of the metadata.
        *   Metadata content (*m* bytes), corresponding to the entire metadata byte stream.
    *   Artifact Package:
        *   Artifact package version (1 byte), corresponding to `index-version` in the index.
        *   Artifact package length (4 bytes), corresponding to the byte length *n* of the artifact package.
        *   Artifact package content (*n* bytes), corresponding to the entire artifact package byte stream.

For example, when uploading version `1.0.0` of the module `demo1` without an organization, `url = /pkg/demo1`. When uploading version `2.0.0` of the module `demo2` within the organization `org`, `url = /pkg/demo2?organization=org`. The version number is not reflected in the url.

## Artifact Package Download

After successfully performing dependency resolution, `cjpm` sends a request to the central repository to download the corresponding artifact package based on the finalized version of each artifact. The corresponding `API` specification is:

*   **Method**: `GET`
*   **`url`**:
    *   Artifact without organization: `/pkg/${module-name}/version`
    *   Artifact within an organization: `/pkg/${module-name}/version?organization=${org-name}`
*   **Returned Data**: Source code archive in `tar.gz` format.

For example, to download the artifact package for version `1.0.0` of artifact `demo1` without an organization, `url = /pkg/demo1/1.0.0`. To download the artifact package for version `2.0.0` of artifact `demo2` within the organization `org`, `url = /pkg/demo2/2.0.0?organization=org`.

## Index Download

During the dependency resolution process or in the `update` command, `cjpm` sends a request to the central repository to download the corresponding artifact index. The corresponding `API` specification is:

*   **Method**: `GET`
*   **`url`**:
    *   Artifact without organization: `/index/${mo}/${du}/${module-name}`
    *   Artifact within an organization: `/index/${mo}/${du}/${module-name}?organization=${org-name}`
*   **Returned Data**: The artifact index file, where each line is a `json` index entry.

For example, to download the index for artifact `aabbcc` without an organization, `url = /index/aa/bb/aabbcc`. To download the index for artifact `dep` within the organization `org`, `url = /index/de/p/dep?organization=org`.

## Response Code Specification

The response code specification for all `APIs` in this chapter is as follows:

*   **200**: Success
*   **400**: Parameter error, possibly due to metadata or index parsing error.
*   **401**: User authentication failed.
*   **403**: User lacks permission.
*   **404**: File does not exist.
*   **409**: Uploaded artifact package conflicts with an existing one in the repository.
*   **\>=500**: Server failure.