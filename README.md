# TeePeople website

Static multi-page site built for GitHub Pages and easy future self-hosting.

## Included pages
- Home
- Members
- Game Servers
- YouTube
- Twitch
- D&D landing page
- Evidence of Absence campaign page
- Character pages for Azarth, Zenko Shadowleaf, Daenalieth Althaea, and Kael Thorne

## Deploying to GitHub Pages
1. Create a new GitHub repository.
2. Upload all files from this folder to the repository root.
3. In GitHub, open **Settings > Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the main branch and the root folder.
6. Save.

## Custom domain
A `CNAME` file is already included for `teepeople.co.uk`.

After GitHub Pages is live:
1. Point your domain DNS to GitHub Pages using the records GitHub gives you.
2. In the repository Pages settings, confirm the custom domain is `teepeople.co.uk`.
3. Enable HTTPS once it becomes available.

## Notes
- Twitch embeds use the current live hostname automatically.
- The YouTube page is set up link-first and is ready for a featured video embed later if you choose one.
- All game server pages avoid exposing private server details by design.

## MrTeemTactics statistical updates

The statistical updater reads `/mrteemtactics/updates/v2/index.json` anonymously. It starts as `unpublished`. After rights review and owner approval, this path can hold signed metadata for immutable statistical assets in a dedicated public GitHub Releases repository. The website hosts only the discovery document. The earlier v1 bootstrap remains unpublished. The application installer is distributed separately.

## Windows download

The menu links to [the latest verified Windows installer](https://teepeople.co.uk/mrteemtactics/download/). GitHub Pages renders the download and its JSON endpoint from `_data/mrteemtactics_windows.json`. The Windows release publisher updates this record after downloading and verifying the versioned MSI.
