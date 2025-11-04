import React from 'react';
import PropTypes from 'prop-types';

// ============================================================================
// 1. ICON COMPONENTS
// In a real-world project, these would likely live in `components/icons/`
// and be exported from a single index file for easier imports.
// ============================================================================

const HomeIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg> );
const CalendarIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg> );
const DocumentIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg> );
const TeamIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.653-.125-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.653.125-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg> );
const CheckCircleIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> );
const PencilIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg> );
const MeetTeamIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M15 21a6 6 0 00-9-5.197M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg> );
const FirstWeekIcon = (props) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}><path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2zM12 18a3 3 0 100-6 3 3 0 000 6z" /></svg> );

// ============================================================================
// 2. GENERIC, REUSABLE UI COMPONENTS
// These are the building blocks of our UI (e.g., Card, ProgressBar).
// ============================================================================

/**
 * A simple progress bar component.
 * @param {object} props - The component props.
 * @param {number} props.percentage - The completion percentage (0-100).
 */
const ProgressBar = ({ percentage }) => (
  <div className="w-48 bg-white/30 rounded-full h-1.5 mt-1">
    <div className="bg-white h-1.5 rounded-full" style={{ width: `${percentage}%` }}></div>
  </div>
);

ProgressBar.propTypes = {
  percentage: PropTypes.number.isRequired,
};

/**
 * A generic card container component for consistent styling.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The content to render inside the card.
 * @param {string} [props.className] - Additional classes to apply to the card.
 */
const Card = ({ children, className = '' }) => (
  <div className={`bg-white rounded-lg shadow-sm border border-slate-200 ${className}`}>
    {children}
  </div>
);

Card.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
};

// ============================================================================
// 3. APPLICATION-SPECIFIC COMPONENTS
// These components are built from the generic components and are specific
// to the features of our dashboard.
// ============================================================================

/**
 * Displays the user's onboarding completion progress.
 * @param {object} props - The component props.
 * @param {number} props.percentage - The completion percentage.
 */
const CompletionProgress = ({ percentage }) => (
  <div className="flex items-center mt-4 space-x-3">
    <div className="bg-white/20 rounded-full p-1">
      <CheckCircleIcon className="text-white h-7 w-7" />
    </div>
    <div>
      <span className="font-medium">{percentage}% Complete</span>
      <ProgressBar percentage={percentage} />
    </div>
  </div>
);

CompletionProgress.propTypes = {
  percentage: PropTypes.number.isRequired,
};


/**
 * The main header for the dashboard.
 * @param {object} props - The component props.
 * @param {string} props.userName - The name of the user.
 * @param {number} props.completionPercentage - The user's onboarding completion percentage.
 */
const DashboardHeader = ({ userName, completionPercentage }) => (
  <header className="bg-gradient-to-r from-blue-600 to-blue-500 rounded-xl p-8 text-white shadow-lg">
    <div className="flex justify-between items-start">
      <div>
        <h1 className="text-3xl font-bold">Welcome to Momentum</h1>
        <CompletionProgress percentage={completionPercentage} />
      </div>
      <div className="text-lg font-medium">Hi, {userName}!</div>
    </div>
  </header>
);

DashboardHeader.propTypes = {
  userName: PropTypes.string.isRequired,
  completionPercentage: PropTypes.number.isRequired,
};


/**
 * A single item in the sidebar navigation.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.icon - The icon component for the nav item.
 * @param {string} props.label - The text label for the nav item.
 * @param {boolean} [props.isActive=false] - Whether the nav item is currently active.
 */
const NavItem = ({ icon, label, isActive = false }) => (
  <li>
    <a href="#" className={`flex items-center py-4 px-4 my-1 rounded-lg text-slate-600 font-medium transition-colors duration-200 ${isActive ? 'bg-slate-100' : 'hover:bg-slate-50'}`}>
      <span className={isActive ? 'text-blue-500' : 'text-slate-400'}>{icon}</span>
      <span className="ml-4">{label}</span>
    </a>
  </li>
);

NavItem.propTypes = {
  icon: PropTypes.node.isRequired,
  label: PropTypes.string.isRequired,
  isActive: PropTypes.bool,
};


/**
 * The sidebar navigation component.
 * @param {object} props - The component props.
 * @param {Array<object>} props.items - An array of navigation item objects.
 */
const SidebarNav = ({ items }) => (
  <aside className="lg:col-span-1">
    <nav>
      <ul>
        {items.map((item) => (
          <NavItem key={item.name} label={item.name} icon={item.icon} isActive={item.active} />
        ))}
      </ul>
    </nav>
  </aside>
);

SidebarNav.propTypes = {
  items: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    icon: PropTypes.node.isRequired,
    active: PropTypes.bool,
  })).isRequired,
};


/**
 * Card displaying upcoming events.
 * @param {object} props - The component props.
 * @param {Array<object>} props.events - An array of event objects.
 */
const UpNextCard = ({ events }) => (
  <Card className="p-6">
    <h2 className="text-xl font-bold text-slate-800 mb-4">Up Next</h2>
    <ul className="space-y-3 list-disc list-inside text-slate-600">
      {events.map((event, index) => (
        <li key={index}>
          <span className="font-semibold">{event.time}</span> - {event.description}
        </li>
      ))}
    </ul>
  </Card>
);

UpNextCard.propTypes = {
  events: PropTypes.arrayOf(PropTypes.shape({
    time: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
  })).isRequired,
};


/**
 * A simple calendar widget.
 * @param {object} props - The component props.
 * @param {Array<string|number>} props.days - An array representing the days of the month.
 * @param {number} props.highlightedDay - The day to highlight.
 */
const CalendarWidget = ({ days, highlightedDay }) => (
  <Card>
    <div className="bg-blue-500 text-white text-center py-3 rounded-t-lg font-semibold">
      WEDNESDAY 16
    </div>
    <div className="p-4">
      <div className="grid grid-cols-7 text-center text-xs text-slate-400 font-bold mb-2">
        <span>Su</span><span>M</span><span>Tu</span><span>We</span><span>Th</span><span>Fr</span><span>Sa</span>
      </div>
      <div className="grid grid-cols-7 text-center text-sm">
        {days.map((day, i) => (
          <div key={i} className={`p-1.5 flex justify-center items-center font-medium ${[4, 11, 18, 25].includes(i) ? 'text-red-400' : 'text-slate-700'}`}>
            {day === highlightedDay ?
              <span className="bg-blue-500 text-white rounded-full h-7 w-7 flex items-center justify-center">{day}</span> :
              <span>{day}</span>
            }
          </div>
        ))}
      </div>
    </div>
  </Card>
);

CalendarWidget.propTypes = {
  days: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number])).isRequired,
  highlightedDay: PropTypes.number.isRequired,
};


/**
 * A single item in the Quick Access section.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.icon - The icon for the item.
 * @param {string} props.name - The name/label for the item.
 */
const QuickAccessItem = ({ icon, name }) => (
  <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 flex flex-col items-center justify-center text-center hover:shadow-md transition-shadow cursor-pointer">
    {icon}
    <span className="mt-2 text-sm font-semibold text-slate-600">{name}</span>
  </div>
);

QuickAccessItem.propTypes = {
  icon: PropTypes.node.isRequired,
  name: PropTypes.string.isRequired,
};


/**
 * Section for Quick Access items.
 * @param {object} props - The component props.
 * @param {Array<object>} props.items - An array of quick access item objects.
 */
const QuickAccessSection = ({ items }) => (
  <div className="xl:col-span-2">
    <h2 className="text-xl font-bold text-slate-800 mb-4">Quick Access</h2>
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
      {items.map((item) => (
        <QuickAccessItem key={item.name} name={item.name} icon={item.icon} />
      ))}
    </div>
  </div>
);

QuickAccessSection.propTypes = {
  items: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    icon: PropTypes.node.isRequired,
  })).isRequired,
};


/**
 * Card displaying information about the onboarding buddy.
 * @param {object} props - The component props.
 * @param {object} props.buddy - The onboarding buddy object.
 * @param {string} props.buddy.name - The buddy's name.
 * @param {string} props.buddy.role - The buddy's role.
 */
const OnboardingBuddyCard = ({ buddy }) => (
  <div className="xl:col-span-1">
    <Card className="p-6 h-full flex flex-col justify-center">
      <div className="flex items-center">
        <div className="bg-slate-200 rounded-full h-16 w-16 flex-shrink-0 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-slate-400" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-4">
          <h3 className="font-semibold text-slate-500 text-sm">Your Onboarding Buddy</h3>
          <p className="font-bold text-slate-800">{buddy.name}</p>
          <p className="text-sm text-slate-500">- {buddy.role}</p>
        </div>
      </div>
    </Card>
  </div>
);

OnboardingBuddyCard.propTypes = {
  buddy: PropTypes.shape({
    name: PropTypes.string.isRequired,
    role: PropTypes.string.isRequired,
  }).isRequired,
};

// ============================================================================
// 4. MAIN PAGE COMPONENT (THE ORCHESTRATOR)
// This component now composes all the smaller pieces together.
// Data is defined here and passed down as props. In a real app, this data
// might come from an API call via a custom hook (e.g., `useOnboardingData`).
// ============================================================================

const OnboardingDashboard = ({
  userName = "Alex Chen",
  completionPercentage = 55,
  onboardingBuddy = { name: "Maria Rodriguez", role: "Software Engineer" },
}) => {
  // Data definitions remain here, but could be fetched from an API
  const navItems = [
    { name: "Dashboard", icon: <HomeIcon />, active: true },
    { name: "My Schedule", icon: <CalendarIcon /> },
    { name: "Resources", icon: <DocumentIcon /> },
    { name: "Team", icon: <TeamIcon /> },
  ];

  const upcomingEvents = [
    { time: "9:00 AM", description: "New Hire Orientation (Virtual)" },
    { time: "11:00 AM", description: "New Hire Orientation (Virtual)" },
    { time: "11:00 AM", description: "Meet Your Manager - Sarah Lee" },
  ];

  const quickAccessItems = [
    { name: "Complete Paperwork", icon: <PencilIcon /> },
    { name: "Meet Your Team", icon: <MeetTeamIcon /> },
    { name: "First Week Schedule", icon: <FirstWeekIcon /> },
  ];

  const calendarDays = ["", "", "", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, ""];

  return (
    <div className="bg-slate-100 min-h-screen p-4 sm:p-6 lg:p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <DashboardHeader userName={userName} completionPercentage={completionPercentage} />

        <main className="mt-[-2rem] bg-white rounded-xl shadow-lg p-6 lg:p-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <SidebarNav items={navItems} />

            <div className="lg:col-span-3">
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                <div className="xl:col-span-2 space-y-6">
                  <UpNextCard events={upcomingEvents} />
                </div>

                <div className="xl:col-span-1">
                  <CalendarWidget days={calendarDays} highlightedDay={10} />
                </div>

                <div className="xl:col-span-3 grid grid-cols-1 xl:grid-cols-3 gap-6">
                  <QuickAccessSection items={quickAccessItems} />
                  <OnboardingBuddyCard buddy={onboardingBuddy} />
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

OnboardingDashboard.propTypes = {
    userName: PropTypes.string,
    completionPercentage: PropTypes.number,
    onboardingBuddy: PropTypes.shape({
        name: PropTypes.string,
        role: PropTypes.string,
    }),
};

export default OnboardingDashboard;