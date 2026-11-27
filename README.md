# TeePeople website

Static Jekyll site for GitHub Pages. The Signal layout and shared navigation
live in `_layouts` and `_includes`.

## Included pages
- Home
- Software catalogue, MrTeemTactics release page and MrTeeTales development page
- Members
- Game Servers
- YouTube
- Twitch
- D&D landing page
- Evidence of Absence campaign page
- Character pages for Azarth, Zenko Shadowleaf, Daenalieth Althaea, and Kael Thorne

## Local preview

With Jekyll 3.10.0 available, run `jekyll serve --safe` from the repository
root and open the local address it prints. The build renders the site layout
and release metadata. Opening the source HTML directly skips that step.

## Custom domain
A `CNAME` file is already included for `teepeople.co.uk`.

After GitHub Pages is live:
1. Point your domain DNS to GitHub Pages using the records GitHub gives you.
2. In the repository Pages settings, confirm the custom domain is `teepeople.co.uk`.
3. Enable HTTPS once it becomes available.

## Notes
- Stream and video embeds load on request. Direct Twitch and YouTube links
  work without JavaScript. Twitch’s player is offered only where its 400 × 300
  minimum size fits.
- All game server pages avoid exposing private server details by design.

## Catalogue and release checks

Each `_data/software.json` entry has a stable `id`, product `path`, category,
summary, description, status, supported platforms, and a `support` link to
a Contact page section. Use `released` or `in_development` for status. A
released entry names its `release` data file and lists at least one platform.
An in-development entry may leave `platforms` empty. Add MrTeemTactics
release notes under `tactics_notes` when they are available.

From the repository root, run the following before publishing:

```text
python _scripts/check_release.py
jekyll build --safe
python _scripts/check_release.py --site _site
```

The Python check uses the standard library. It validates catalogue fields,
product routes and support links, and compares the MrTeemTactics website
release record with the application feed. With `--site`, it also checks the
generated product and download links, the four JSON feeds, and that the
checker stays out of the generated site. Verify the uploaded installer and
its signature separately.

## MrTeemTactics statistical updates

The statistical updater reads `/mrteemtactics/updates/v2/index.json` anonymously. It starts as `unpublished`. After rights review and owner approval, this path can hold signed metadata for immutable statistical assets in a dedicated public GitHub Releases repository. The website hosts only the discovery document. The earlier v1 bootstrap remains unpublished. The application installer is distributed separately.

## Windows download

The [MrTeemTactics product page](https://teepeople.co.uk/software/mrteemtactics/)
shows the version, platform, package size and SHA-256 before visitors choose
to download. The legacy [download URL](https://teepeople.co.uk/mrteemtactics/download/)
also requires an explicit click to start the download. GitHub Pages renders both
pages and the legacy download JSON endpoint from
`_data/mrteemtactics_windows.json`. The Windows release publisher updates
that record after downloading and verifying the versioned MSI.
