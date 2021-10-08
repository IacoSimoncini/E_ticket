// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

import "./Ownable.sol";

contract Event is Ownable{
    
    uint256 private numTicketsAvailable;

    uint256 private length = 0;
    
    uint256 private numTicketsTotal;
    
    uint256 private eventId;
    
    string private nameEvent;
    
    string private locationEvent;
    
    uint256 private ticketPrice;
    
    bool private deleted;

    
    struct Tickets{
        string taxSeal; // Generated outside the smart contract (inside the smart contract could be risky)
        uint256 ticketID;
        bool valid;
    }

    mapping (address => Tickets[]) public ticket;

    Tickets[] refund_list; 
    /**
     * Constructor that creates tickets when the event is created
     *
     * @param _eventId uint256 event's ID
     * @param _numTicketsAvailable uint256 number of tickets available for a single event
     * @param _nameEvent string event's name
     * @param _locationEvent string event's location
     * @param _ticketPrice uint256 ticket's price
    **/
    constructor(uint256 _eventId, 
        uint256 _numTicketsAvailable, 
        string memory _nameEvent, 
        string memory _locationEvent, 
        uint256 _ticketPrice) 
    {
        numTicketsAvailable = _numTicketsAvailable;
        numTicketsTotal = _numTicketsAvailable;
        eventId = _eventId;
        nameEvent = _nameEvent;
        locationEvent = _locationEvent;
        ticketPrice = _ticketPrice;
        deleted = false;
    }
    
    /**
     * Getter methods
    **/
    
    function getEventId() public view returns(uint256){
        return eventId;
    }
    
    function getNumTicketsAvailable() public view returns(uint256){
        return numTicketsAvailable;
    }
    
    function getNameEvent() public view returns(string memory){
        return nameEvent;
    }
    
    function getLocationEvent() public view returns(string memory){
        return locationEvent;
    }
    
    function getTicketPrice() public view returns(uint256) {
        return ticketPrice;
    }
    
    function isDeleted() public view returns(bool){
        return deleted;
    }

    function getTickets(address _ticketOwner) public view returns(Tickets[] memory){
        return ticket[_ticketOwner];
    }

    function getTotalTickets() public view returns(uint256){
        return numTicketsTotal;
    }

    function getSoldTickets() public view returns(uint256){
        return numTicketsTotal - numTicketsAvailable;
    }


    /**
     * Setter methods
    **/

   
    function deleteEvent(uint256 _eventID) onlyOwner public returns(bool) {
        if (eventId == _eventID){
            deleted = true;
            return true;
        } else {
            return false;
        }
    }

    function setValues (uint256 num_ticket, string memory nome,string memory luogo,uint256 prezzo) public returns(bool){
        numTicketsAvailable = numTicketsAvailable+num_ticket-numTicketsTotal;
        numTicketsTotal = num_ticket;
        nameEvent = nome;
        locationEvent = luogo;
        ticketPrice = prezzo;
        return true;
    }
    
    /**
     * Events 
    **/
    event BuyTicketEvent(address buyer, uint256 ticketID);
    
    /**
     * Functions
    **/
    function createTicket(address buyer, string memory _taxSeal) public returns(uint256){
        uint256 _ticketID = length;
        length++;
        Tickets memory _ticket = Tickets({
            ticketID: _ticketID,
            taxSeal: _taxSeal,
            valid: true
        });
        ticket[buyer].push(_ticket);
        return _ticketID;
    }
    
    function buyTicket(address buyer, string memory _taxSeal) public returns(bool){
        numTicketsAvailable -= 1;
        uint256 _ticketID;
        if(refund_list.length!=0){
            ticket[buyer].push(refund_list[refund_list.length-1]);
            _ticketID=refund_list[refund_list.length-1].ticketID;
            refund_list.pop();
        }
        else
            _ticketID = createTicket(buyer, _taxSeal);
        emit BuyTicketEvent(buyer, _ticketID);
        return true;
    }
    
    function invalidation(address owner, uint256 relativeID) onlyOwner public returns(bool){
        if (ticket[owner][relativeID].valid == true) {
            ticket[owner][relativeID].valid = false;
            return true;
        }
        return false;
    }
    
    function refundTicket(address owner,uint256 relativeID) public returns(bool){
        
        if(ticket[owner][relativeID].valid){
            refund_list.push(ticket[owner][relativeID]);           
            for (uint i = relativeID; i<ticket[owner].length-1; i++){
                ticket[owner][i].taxSeal = ticket[owner][i+1].taxSeal;
                ticket[owner][i].valid = ticket[owner][i+1].valid;
                ticket[owner][i].ticketID = ticket[owner][i+1].ticketID;
            }
            ticket[owner].pop();
            numTicketsAvailable+=1;
            return true;
        }
        else return false;
    }
    
    
}