# Radio Bretzel Team

Radio Bretzel Team Module is the core backend module of Radio Bretzel application.
An instance represent a Radio Bretzel Team, and allow its Chief to manage Members,
Channels, Sources, and chat operations. It's also an identity and authorization
server for `rb-trackman` and `rb-streamer` modules.

## Install
Note that this install methods are intendeed to the `rb-team` Radio Bretzel module.
If you want to install full Radio Bretzel application, please refer to the app
[documentation](https://docs.radiobretzel.org)

### Requirements
    * `python3`
    * `pip3`

### Using `pip`
```bash
$ git clone https://source.radiobretzel.org/app/rb-team.git
$ pip install ./rb-team
```

### Run with `docker`
Radio Bretzel Team module can be installed with docker using image `registry.radiobretzel.org/rb-team:latest`.
Note that this image will not run entire Radio Bretzel application but jsut the `rb-team` module.
If you want to run Radio Bretzel full application using `docker`, checkout the [documentation](https://docs.radiobretzel.org).

## Documentation
### User Documentation
User documentation is available [here](https://docs.radiobretzel.org)

### Admin Documentation
Admin documentation is available [here](https://docs.radiobretzel.org/admin/rb-team)

### API
`rb-team` API is compliant to the [Open-API v3](https://www.openapis.org/).
An API reference is available [here](https://docs.radiobretzel.org/rb-team/api_reference).

## Security Concerns
This module handles Authentication and Authorization processes using [JSON Web Tokens](https://jwt.io).
This technology is known for being cypher-dependant, and requires an HTTPS connection
to be considered as secure session management process.
