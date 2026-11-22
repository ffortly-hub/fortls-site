# fortls-tools

Browser-only helper logic behind the free tools on [fortls.com](https://fortls.com): a `.fortls` generator, a `.fortls` validator (JSONC aware), an `fpm.toml` generator and a VS Code settings generator.

- `src/tools.js` — generators and validator (plain JavaScript, no dependencies, no network).
- `rules/fortls-keys.json` — option names and value types the validator knows.

**Independent project.** Not the official fortls project and not affiliated with the fortls maintainers or the Fortran-lang organization. Generated output is provided as-is; review it against the official documentation.

Licence: MIT. The FORTLS website design, logos, articles and domain assets are not part of this repository.
