from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models


def get_challenge_quota(db: Session, user_id: str) -> models.ChallengeQuota:
    """
    Retrieves the challenge quota for a specific user.
    
    Args:
        db (Session): The database session.
        user_id (str): The ID of the user whose quota is to be retrieved.
        
    Returns:
        ChallengeQuota: The challenge quota for the specified user.
    """
    return db.query(models.ChallengeQuota).filter(models.ChallengeQuota.user_id == user_id).first()


def create_challenge_quota(db: Session, user_id: str) -> models.ChallengeQuota:
    """
    Creates a new challenge quota for a user.
    
    Args:
        db (Session): The database session.
        user_id (str): The ID of the user for whom the quota is to be created.
        
    Returns:
        ChallengeQuota: The newly created challenge quota.
    """
    quota = models.ChallengeQuota(user_id=user_id)
    db.add(quota)
    db.commit()
    db.refresh(quota)
    return quota


def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota) -> models.ChallengeQuota:
    """
    Resets the challenge quota if the last reset date is more than 24 hours ago.
    
    Args:
        db (Session): The database session.
        quota (ChallengeQuota): The challenge quota to check and potentially reset.
    Returns:
        ChallengeQuota: The updated challenge quota after checking/resetting.
    """
    now = datetime.now()
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.remaining_quota = 50
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    return quota


def create_challenge(
    db: Session, 
    difficulty: str, 
    created_by: str, 
    title: str, 
    options: str, 
    correct_answer_id: int, 
    explanation: str
) -> models.Challenge:
    """
    Creates a new challenge in the database.
    
    Args:
        db (Session): The database session.
        difficulty (str): The difficulty level of the challenge.
        created_by (str): The user ID of the creator.
        title (str): The title of the challenge.
        options (str): The options for the challenge.
        correct_answer_id (int): The ID of the correct answer.
        explanation (str): Explanation for the challenge.
        
    Returns:
        Challenge: The newly created challenge.
    """
    challenge = models.Challenge(
        difficulty=difficulty,
        created_by=created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


def get_user_challenges(db: Session, user_id: str):
    """
    Retrieves all challenges created by a specific user.
    
    Args:
        db (Session): The database session.
        user_id (str): The ID of the user whose challenges are to be retrieved.
        
    Returns:
        list: A list of challenges created by the specified user.
    """
    return db.query(models.Challenge).filter(models.Challenge.created_by == user_id).all()
