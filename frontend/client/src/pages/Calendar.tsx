import React from 'react';
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'

function Calendar() {
  return (
    <div>
      <div className='ml-5 mr-5 mx-auto'>
        <FullCalendar plugins={[ dayGridPlugin ]} initialView="dayGridMonth" />
      </div>
    </div>
  );
}

export default Calendar;