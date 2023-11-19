def form_courses(groups: list[str]):
    courses: set[int] = set()
    for group in groups:
        course = int(group[0])
        courses.add(course)
    return list(sorted(courses))
