# Maintaining the alumni directory

Edit Resources/people/Alumni.json. Each category contains a people array:

```json
{"name":"Example Student","role":"Ph.D.","duration":"2026","destination":"First employer"}
```

Keep the four categories in their existing order. duration is the displayed Year; destination is First Employment. For the existing Post-Docs & Visiting Researchers records, destination preserves the next position after leaving the lab.

To graduate a current member:
1. Move their entry from Current.json to the appropriate Alumni.json category and add duration and destination. Do not invent missing employment information; an empty value displays a dash.
2. Move their entire Resources/people/Current/First_Last folder to Resources/people/Alumni/First_Last. Keep intro.json, photo and contact fields unchanged. The folder name is the person's name with spaces replaced by underscores.
3. Preview people_alumni.html. Members with profile assets have a clickable name; details open inline. Members without profile assets remain plain text.
4. Commit Resources and update the parent repository's submodule pointer when ready to publish.

The website preserves all profile files; alumni profiles display biography, research interests, photo and contact links without an individual publication list.
