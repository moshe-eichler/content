To create an Incident Reporting API Web Service role and user.
Log on to the Enforce Server administration console as an Administrator.
1. Select System > Login Management > Roles.
2. Click Add Role.
3. Type a name for the new role in the Name field. For example, type “Incident API Client Role.”
4. In the User Privileges section of the screen, select the items: View, Actions, API, Display Attributes,
Custom Attributes
5. (Optional) Click the Incident Access tab to set additional conditions that limit the incidents that Incident Reporting and Update
API clients may access.
6. Click Save.
7. Select System > Login Management > DLP Users.
8. Click Add DLP User.
9. Type the credentials for the new user in the Name, Password, and Re-enter Password fields.
10. In the Roles section of the screen, select the new role you created. For example, select “Incident API Client Role.”
11. Select the same Incident API Client Role in the Default Role menu. 
12. Click Save.