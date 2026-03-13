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
