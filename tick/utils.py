import datetime
from .models import Event
import tick.contracts.smart_contract as sc

def setup(w3, abi):
    events = Event.objects.all()
    current_date = datetime.date.today()
    #yesterday = current_date - datetime.timedelta(days=1)
    #c_date = yesterday.strftime("%Y-%m-%d")
    c_date = current_date.strftime("%Y-%m-%d")
    filtered_events = events.filter(data_evento__range=["1998-12-13","1999-12-12"])
    for f in filtered_events:
        contract_event = sc.deploy_contract(f.address, abi, w3)
        event = Event.objects.get(id=f.id)
        event.delete()
        sc.delete_event(contract_event, f.id, w3)