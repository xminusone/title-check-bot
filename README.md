# title-check-bot
Reddit bot that removes unmoderated submissions with incorrect titles.
## How does it work?
* Rather than checking against the HTML <title> element or the <h1> tag for the page, TitleCheckBot simply takes the Reddit submission title and verifies that it exists somewhere on the linked page.  While this does cause some false negatives, it avoids most false positives.
## What sites can it check?
TitleCheckBot can check most Reddit submissions.  However, some sites that are bot unfriendly cannot be checked.  TitleCheckBot automatically ignores submissions that generate a standard error when it is checked, and sites that are incompatible in other ways are listed in exemptions.cfg.  Sites found to be incompatible can be added to exemptions.cfg.  The bot must be restarted after adding an exemption.
