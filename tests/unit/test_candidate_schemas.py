from job_market.interfaces.schemas.candidates import CandidateProfileRequest


def test_candidate_profile_deduplicates_trimmed_skill_names_case_insensitively() -> None:
    profile = CandidateProfileRequest.model_validate(
        {
            "summary": "Synthetic software engineer.",
            "skills": [
                {"name": " Python ", "proficiency": " advanced "},
                {"name": "python", "proficiency": "beginner"},
                {"name": "SQL"},
            ],
        }
    )

    assert [skill.name for skill in profile.skills] == ["Python", "SQL"]
    assert profile.skills[0].proficiency == "advanced"
