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
- Update the catalogue in `_data/software.json`. Its released entries read
  their version from the associated release data file. Add version-specific
  release notes under `tactics_notes` when they are available.

## MrTeemTactics statistical updates

The statistical updater reads `/mrteemtactics/updates/v2/index.json` anonymously. It starts as `unpublished`. After rights review and owner approval, this path can hold signed metadata for immutable statistical assets in a dedicated public GitHub Releases repository. The website hosts only the discovery document. The earlier v1 bootstrap remains unpublished. The application installer is distributed separately.

## Windows download

The [MrTeemTactics product page](https://teepeople.co.uk/software/mrteemtactics/)
shows the version, platform, package size and SHA-256 before visitors choose
to download. The legacy [download URL](https://teepeople.co.uk/mrteemtactics/download/)
still starts the installer download automatically. GitHub Pages renders both
pages and the legacy download JSON endpoint from
`_data/mrteemtactics_windows.json`. The Windows release publisher updates
that record after downloading and verifying the versioned MSI.
