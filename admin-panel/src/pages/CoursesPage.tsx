import React, { useEffect, useState } from 'react';
import { courseApi } from '../api/courseApi';

const CoursesPage: React.FC = () => {
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
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

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Quản lý Khóa học</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
          + Thêm khóa học
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center p-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <div key={course.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">{course.name}</h2>
              <p className="text-gray-600 mb-4 line-clamp-2">{course.description}</p>
              <div className="flex justify-between items-center text-sm text-gray-500">
                <span>{course.lessons?.length || 0} bài học</span>
                <button className="text-blue-600 hover:text-blue-800 font-medium">Chi tiết →</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CoursesPage;
