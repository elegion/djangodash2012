def can_edit_project(user, project):
    return user.fortuitusprofile.company == project.company
