import React, { useEffect, useState, useRef } from 'react';
import { 
  Plus, 
  FileJson, 
  ChevronRight, 
  Search, 
  BookOpen, 
  Layers, 
  Subtitles,
  Music,
  Trash2,
  Edit2
} from 'lucide-react';
import { courseApi } from '../api/courseApi';
import type { Course, Lesson } from '../types/course';
import CourseBreadcrumbs from '../components/CourseBreadcrumbs';

type ViewMode = 'courses' | 'lessons' | 'words';

const CoursesPage: React.FC = () => {
  const [viewMode, setViewMode] = useState<ViewMode>('courses');
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    setLoading(true);
    try {
      const response = await courseApi.getCourses();
      if (response.data.code === 200) {
        setCourses(response.data.data);
      }
    } catch (error) {
      console.error('Failed to fetch courses', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCourseClick = async (course: Course) => {
    setLoading(true);
    try {
      const response = await courseApi.getCourseDetail(course.id);
      if (response.data.code === 200) {
        setSelectedCourse(response.data.data);
        setViewMode('lessons');
      }
    } catch (error) {
      console.error('Failed to fetch course detail', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLessonClick = (lesson: Lesson) => {
    setSelectedLesson(lesson);
    setViewMode('words');
  };

  const handleImportJson = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const data = JSON.parse(event.target?.result as string);
        console.log('Importing data:', data);
        alert('Tính năng Import hàng loạt đang được xử lý ở Backend. Dữ liệu đã được đọc thành công!');
      } catch (err) {
        alert('File JSON không hợp lệ!');
      }
    };
    reader.readAsText(file);
  };

  const breadcrumbItems = [
    ...(selectedCourse ? [{ 
      label: selectedCourse.name, 
      onClick: () => { setViewMode('lessons'); setSelectedLesson(null); } 
    }] : []),
    ...(selectedLesson ? [{ label: selectedLesson.name }] : [])
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto min-h-screen">
      {/* Header Area */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <BookOpen className="text-brand-500" size={32} />
            {viewMode === 'courses' ? 'Quản lý Khóa học' : 
             viewMode === 'lessons' ? 'Danh sách Bài học' : 'Từ vựng trong bài'}
          </h1>
          <p className="text-slate-400 mt-1">Hệ thống quản trị nội dung Vocabulary</p>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleImportJson}
            accept=".json"
            className="hidden"
          />
          <button 
            onClick={() => fileInputRef.current?.click()}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 transition-colors text-sm font-medium"
          >
            <FileJson size={18} className="text-amber-400" />
            Import JSON
          </button>
          <button className="btn-primary flex items-center gap-2 px-5 py-2.5 text-sm">
            <Plus size={18} />
            Thêm mới
          </button>
        </div>
      </div>

      {/* Navigation & Search */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <CourseBreadcrumbs 
          items={breadcrumbItems} 
          onHomeClick={() => { 
            setViewMode('courses'); 
            setSelectedCourse(null); 
            setSelectedLesson(null); 
          }} 
        />
        
        <div className="relative group">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-brand-400 transition-colors" size={18} />
          <input 
            type="text" 
            placeholder="Tìm kiếm nhanh..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-dark pl-10 pr-4 py-2 text-sm w-full md:w-64"
          />
        </div>
      </div>

      {/* Content Area */}
      {loading ? (
        <div className="flex flex-col items-center justify-center p-20 gap-4">
          <div className="w-12 h-12 border-4 border-brand-500/20 border-t-brand-500 rounded-full animate-spin"></div>
          <p className="text-slate-400 text-sm animate-pulse">Đang tải dữ liệu...</p>
        </div>
      ) : (
        <div className="animate-fade-up">
          {/* COURSE LIST VIEW */}
          {viewMode === 'courses' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.filter(c => c.name.toLowerCase().includes(searchTerm.toLowerCase())).map((course) => (
                <div 
                  key={course.id} 
                  onClick={() => handleCourseClick(course)}
                  className="glass-card p-6 cursor-pointer group hover:scale-[1.02] transition-all duration-300"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="p-3 rounded-2xl bg-brand-500/10 text-brand-400 group-hover:bg-brand-500 group-hover:text-white transition-colors duration-500">
                      <Layers size={24} />
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button className="p-2 hover:bg-white/10 rounded-lg text-slate-400 hover:text-white"><Edit2 size={16} /></button>
                      <button className="p-2 hover:bg-red-500/20 rounded-lg text-slate-400 hover:text-red-400"><Trash2 size={16} /></button>
                    </div>
                  </div>
                  <h2 className="text-xl font-bold text-white mb-2 group-hover:text-brand-400 transition-colors">{course.name}</h2>
                  <p className="text-slate-400 text-sm line-clamp-2 mb-4 h-10">{course.description}</p>
                  <div className="flex items-center justify-between pt-4 border-t border-white/5 text-xs font-medium text-slate-500">
                    <span className="flex items-center gap-1.5 ring-1 ring-white/5 px-2 py-1 rounded-md">
                      {course.lessons?.length || 0} bài học
                    </span>
                    <span className="group-hover:translate-x-1 transition-transform flex items-center gap-1 text-brand-400">
                      Chi tiết <ChevronRight size={14} />
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* LESSON LIST VIEW */}
          {viewMode === 'lessons' && selectedCourse && (
            <div className="space-y-4">
              {selectedCourse.lessons.filter(l => l.name.toLowerCase().includes(searchTerm.toLowerCase())).map((lesson) => (
                <div 
                  key={lesson.id}
                  onClick={() => handleLessonClick(lesson)}
                  className="glass-card p-5 flex flex-col md:flex-row items-center justify-between gap-4 cursor-pointer hover:bg-white/[0.03] transition-colors border-l-4 border-transparent hover:border-brand-500"
                >
                  <div className="flex items-center gap-5 flex-1 w-full">
                    <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center text-brand-400 shrink-0">
                      <Subtitles size={24} />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white">{lesson.name}</h3>
                      <p className="text-brand-400 text-sm font-medium">{lesson.subName || 'Chưa có tên phụ'}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-8 w-full md:w-auto justify-between md:justify-end">
                    <div className="text-center">
                      <div className="text-sm font-bold text-white">{lesson.words?.length || lesson.quantityOfWord}</div>
                      <div className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Từ vựng</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button className="p-2.5 hover:bg-white/10 rounded-xl text-slate-400"><Edit2 size={18} /></button>
                      <button className="p-2.5 hover:bg-red-500/10 rounded-xl text-red-500/70"><Trash2 size={18} /></button>
                      <ChevronRight className="text-slate-700 ml-2" size={24} />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* WORD LIST VIEW */}
          {viewMode === 'words' && selectedLesson && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {selectedLesson.words?.filter(w => w.english.toLowerCase().includes(searchTerm.toLowerCase())).map((word) => (
                <div 
                  key={word.id}
                  className="glass-card p-5 border border-white/5 hover:border-brand-500/30 transition-colors relative group"
                >
                  <div className="flex justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <h4 className="text-xl font-black text-white">{word.english}</h4>
                      <span className="text-xs px-2 py-0.5 rounded bg-brand-500/10 text-brand-400 font-bold uppercase tracking-tighter">
                        {word.partOfSpeech}
                      </span>
                    </div>
                    <div className="flex gap-2">
                      {word.audioUrl && (
                        <a href={word.audioUrl} target="_blank" rel="noreferrer" className="p-1.5 rounded-lg bg-blue-500/10 text-blue-400 hover:bg-blue-500 hover:text-white transition-colors">
                          <Music size={14} />
                        </a>
                      )}
                      <button className="p-1.5 rounded-lg hover:bg-white/10 text-slate-500 hover:text-white"><Edit2 size={14} /></button>
                    </div>
                  </div>
                  
                  <div className="text-sm text-slate-300 mb-3 font-medium italic text-brand-400/80">
                    {word.phonetic}
                  </div>

                  <div className="space-y-3">
                    {word.meanings.map((meaning, idx) => (
                      <div key={idx} className="bg-white/5 rounded-lg p-3 text-sm">
                        <div className="font-bold text-slate-200 mb-1 flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-brand-500"></span>
                          {meaning.vietnamese}
                        </div>
                        {meaning.exampleEn && (
                          <div className="text-slate-400 text-xs mt-1 leading-relaxed">
                            "{meaning.exampleEn}"
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 flex justify-between items-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <span className="text-[10px] text-slate-600 font-bold tracking-widest uppercase">ID: {word.id}</span>
                    <span className="text-[10px] text-brand-500/50 font-bold">{word.cefr || 'General'}</span>
                  </div>
                </div>
              ))}
              <div className="glass-card p-5 border-2 border-dashed border-white/5 flex flex-col items-center justify-center gap-3 cursor-pointer hover:bg-white/5 transition-colors group">
                <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 group-hover:bg-brand-500 group-hover:text-white transition-all">
                  <Plus size={20} />
                </div>
                <span className="text-sm font-bold text-slate-500 group-hover:text-slate-300">Thêm từ vựng mới</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CoursesPage;
