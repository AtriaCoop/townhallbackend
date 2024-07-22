from .dao import VolunteerDao as volunteer_dao
from .dao import OpportunityDao as opportunity_dao
from .types import CreateVolunteerData
from .types import CreateOpportunityData
from .models import Volunteer
from .models import Opportunity

class VolunteerServices:
    def get_volunteer(id: int) -> Volunteer:
        return volunteer_dao.get_volunteer(id=id)
    
    def create_volunteer(create_volunteer_data: CreateVolunteerData) -> None:
        return volunteer_dao.create_volunteer(create_volunteer_data=create_volunteer_data)
    
    def delete_volunteer(id: int) -> None:
        volunteer_dao.delete_volunteer(volunteer_id=id)
        
class OpportunityServices:

    def get_opportunity(id: int) -> Opportunity:
        return opportunity_dao.get_opportunity(id=id)
    
    def create_opportunity(create_opportunity_data: CreateOpportunityData) -> None:
        return opportunity_dao.create_opportunity(create_opportunity_data=create_opportunity_data)
