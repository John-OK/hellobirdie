from django.db import models


class Bird(models.Model):
    # required fields
    genus = models.CharField(max_length=50, null=False)
    species = models.CharField(max_length=50, null=False)
    english_name = models.CharField(
        max_length=75, null=False, verbose_name="English Name"
    )

    # optional fields
    subspecies = models.CharField(max_length=50, null=True)
    family = models.CharField(max_length=50, null=True)

    def _format_name_part(self, name_part, separator):
        """Helper method to format name parts with proper capitalization"""
        parts = name_part.lower().split(separator)
        parts[0] = parts[0].title()
        return separator.join(parts)

    def __str__(self):
        scientific_name = f"{self.genus.title()} {self.species.lower()}"

        if self.subspecies:
            scientific_name += f" {self.subspecies.lower()}"

        common_name = self.english_name.title()

        # Proper case for english_name with or without hyphens
        if "-" in common_name:
            names = common_name.split(" ")
            fixed_names = []

            for name in names:
                if "-" in name:
                    fixed_names.append(self._format_name_part(name, "-"))
                else:
                    fixed_names.append(name)
            common_name = " ".join(fixed_names)

        if "'" in common_name:
            names = common_name.split(" ")
            fixed_names = []

            for name in names:
                if "'" in name:
                    fixed_names.append(self._format_name_part(name, "'"))
                else:
                    fixed_names.append(name)
            common_name = " ".join(fixed_names)

        return f"{common_name} ({scientific_name})"
