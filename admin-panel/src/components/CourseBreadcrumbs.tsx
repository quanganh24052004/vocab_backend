import React from 'react';
import { ChevronRight, Home } from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  onClick?: () => void;
}

interface CourseBreadcrumbsProps {
  items: BreadcrumbItem[];
  onHomeClick: () => void;
}

const CourseBreadcrumbs: React.FC<CourseBreadcrumbsProps> = ({ items, onHomeClick }) => {
  return (
    <nav className="flex items-center space-x-2 text-sm text-slate-400 mb-6 animate-fade-up">
      <button 
        onClick={onHomeClick}
        className="flex items-center hover:text-brand-400 transition-colors"
      >
        <Home size={16} className="mr-1" />
        <span>Danh sách</span>
      </button>
      
      {items.map((item, index) => (
        <React.Fragment key={index}>
          <ChevronRight size={14} className="text-slate-600" />
          <button
            onClick={item.onClick}
            disabled={!item.onClick}
            className={`transition-colors ${
              item.onClick ? 'hover:text-brand-400' : 'text-slate-200 cursor-default font-semibold'
            }`}
          >
            {item.label}
          </button>
        </React.Fragment>
      ))}
    </nav>
  );
};

export default CourseBreadcrumbs;
