# WP-CLI reference (operational playbook)

## Golden rules
- Always take a backup/snapshot before destructive ops (updates, deletes, DB changes).
- Prefer staging first for theme/plugin updates.
- Keep changes minimal: update one dimension at a time (core vs plugins vs themes).

## Common commands

### Version / info
- `wp --info`
- `wp core version`

### Core
- `wp core check-update`
- `wp core update`

### Plugins
- `wp plugin list`
- `wp plugin status <slug>`
- `wp plugin update --all`
- `wp plugin deactivate <slug>`

### Themes
- `wp theme list`
- `wp theme update --all`

### Users
- `wp user list`
- `wp user create <user> <email> --role=editor`

### Database
- `wp db export backup.sql`
- `wp db import backup.sql`

### Search/replace (dangerous)
- `wp search-replace 'http://old' 'https://new' --all-tables --precise`

## Health checks
- `wp core verify-checksums`
- `wp plugin list --update=available`
- `wp theme list --update=available`

## Running wp-cli
- If you have multiple sites: use `--path=/var/www/site` (or the site path).
- If your web user differs: you may need `sudo -u www-data wp ...`.
