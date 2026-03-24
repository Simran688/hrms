import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { employeeAPI, attendanceAPI } from '../services/api';
import { useApi, useMutation } from '../hooks/useApi';

const AttendanceForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    employee_id: '',
    date: new Date().toISOString().split('T')[0],
    status: 'present',
  });
  const [errors, setErrors] = useState({});

  const { data: employees, loading: loadingEmployees } = useApi(employeeAPI.getAll);
  const { mutate: markAttendance, loading, error } = useMutation(attendanceAPI.create);

  // Show error toast when mutation error occurs
  useEffect(() => {
    if (error) {
      toast.error(error);
    }
  }, [error]);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.employee_id) {
      newErrors.employee_id = 'Employee is required';
    }
    
    if (!formData.date) {
      newErrors.date = 'Date is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('Please fix the form errors before submitting');
      return;
    }
    
    try {
      await markAttendance(formData);
      toast.success('Attendance marked successfully!');
      onSuccess && onSuccess();
      // Reset form
      setFormData({
        employee_id: '',
        date: new Date().toISOString().split('T')[0],
        status: 'present',
      });
    } catch (err) {
      // Error is handled by useMutation hook and shown via toast
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  if (loadingEmployees) {
    return (
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-center items-center h-32">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-6">Mark Attendance</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="employee_id" className="block text-sm font-medium text-gray-700">
            Employee
          </label>
          <select
            id="employee_id"
            name="employee_id"
            value={formData.employee_id}
            onChange={handleChange}
            className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
              errors.employee_id ? 'border-red-300' : 'border-gray-300'
            }`}
          >
            <option value="">Select Employee</option>
            {employees?.map((employee) => (
              <option key={employee.id} value={employee.employee_id}>
                {employee.employee_id} - {employee.full_name}
              </option>
            ))}
          </select>
          {errors.employee_id && (
            <p className="mt-1 text-sm text-red-600">{errors.employee_id}</p>
          )}
        </div>

        <div>
          <label htmlFor="date" className="block text-sm font-medium text-gray-700">
            Date
          </label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            max={new Date().toISOString().split('T')[0]}
            className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
              errors.date ? 'border-red-300' : 'border-gray-300'
            }`}
          />
          {errors.date && (
            <p className="mt-1 text-sm text-red-600">{errors.date}</p>
          )}
        </div>

        <div>
          <label htmlFor="status" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <div className="mt-2 space-y-2">
            <label className="flex items-center">
              <input
                type="radio"
                id="present"
                name="status"
                value="present"
                checked={formData.status === 'present'}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-700">Present</span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                id="absent"
                name="status"
                value="absent"
                checked={formData.status === 'absent'}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-700">Absent</span>
            </label>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Marking...' : 'Mark Attendance'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AttendanceForm;
