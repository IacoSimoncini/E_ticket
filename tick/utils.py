import datetime
from .models import Event
def setup(sc,w3,abi,):
    events = Event.objects.all()
    current_date=datetime.date.today()
    yesterday=current_date-datetime.timedelta(days=1)
    c_date=yesterday.strftime("%Y-%m-%d")
    filtered_events=events.filter(data_evento__range=["0-1-1",c_date])

    for f in filtered_events:
        contract_event=sc.deploy_contract(f.address, abi, w3)
        sc.delete_event(contract_event,f.id,w3)