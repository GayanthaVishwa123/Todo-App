'use client';

import { useState, useEffect } from 'react';
import axios, { AxiosResponse } from 'axios';
import TaskTable from '@/components/task/TaskTable';
import TaskForm from '@/components/task/TaskForm';
import { Task } from '@/types/task';
import '@/styles/dashboard.css'
export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_URL = 'http://127.0.0.1:8000'; 
  const token = localStorage.getItem('authToken'); 

  // Fetch tasks from the backend
  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/tasks/`, {
        headers: { Authorization: `Bearer ${token}` }, 
      });
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setError('Failed to load tasks.');
    }
  };

  // Fetch tasks when the component mounts or when the token changes
  useEffect(() => {
    if (token) {
      fetchTasks();
    } else {
      setError('Not authenticated.');
    }
  }, [token]);

  // Handle task saving (either update or create)
  const handleSave = async (task: Task) => {
    try {
      // Validate task before proceeding
      if (!task.title) {
        return alert('Title is required');
      }

      let response: AxiosResponse<any, any, {}>;

      if (task.id) {
        // If editing, update existing task (PUT request)
        response = await axios.put(`${API_URL}/tasks/update/${task.id}`, task, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 200) {
          setTasks((prev) => prev.map((t) => (t.id === task.id ? response.data : t)));
        }
      } else {
        // If new task, create a new one (POST request)
        response = await axios.post(`${API_URL}/tasks/create`, task, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 201) {
          setTasks((prev) => [...prev, response.data]);
        }
      }

      setSelectedTask(null); // Close the form after saving
      fetchTasks(); // Re-fetch tasks to ensure the list is updated with latest data
    } catch (error) {
      console.error('Error saving task:', error);
      setError('Failed to save task.');
    }
  };

  // Handle task editing
  const handleEdit = (task: Task) => setSelectedTask(task);

  // Handle task deletion
  const handleDelete = async (id: number) => {
    try {
      const response = await axios.delete(`${API_URL}/tasks/delete/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.status === 200) {
        setTasks((prev) => prev.filter((task) => task.id !== id));
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      setError('Failed to delete task.');
    }
  };

  // Handle task completion
  const handleComplete = async (id: number) => {
    try {
      const taskToUpdate = tasks.find((task) => task.id === id);
      if (taskToUpdate) {
        const updatedTask = { ...taskToUpdate, completed: true };
        const response = await axios.put(`${API_URL}/tasks/complete/${id}`, updatedTask, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 200) {
          setTasks((prev) =>
            prev.map((task) => (task.id === id ? updatedTask : task))
          );
        }
      }
    } catch (error) {
      console.error('Error marking task as completed:', error);
      setError('Failed to mark task as completed.');
    }
  };

  // Handle undo completion
  const handleUndo = async (id: number) => {
    try {
      const taskToUpdate = tasks.find((task) => task.id === id);
      if (taskToUpdate) {
        const updatedTask = { ...taskToUpdate, completed: false };
        const response = await axios.put(`${API_URL}/tasks/Undocomplete/${id}`, updatedTask, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 200) {
          setTasks((prev) =>
            prev.map((task) => (task.id === id ? updatedTask : task))
          );
        }
      }
    } catch (error) {
      console.error('Error undoing task completion:', error);
      setError('Failed to undo task completion.');
    }
  };

  // Filter completed tasks and pending tasks
  const completedTasks = tasks.filter((task) => task.completed);
  const pendingTasks = tasks.filter((task) => !task.completed);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between mb-6">
        <h1 className="text-3xl font-semibold">Task Dashboard</h1>
        <button
          onClick={() =>
            setSelectedTask({
              id: 0,
              title: '',
              deadline: '',
              priority: 'Medium',
              comments: '',
              completed: false,
            })
          }
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          + Task
        </button>
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      <div className="mb-6">
        <h2 className="text-2xl font-semibold mb-4">Pending Tasks</h2>
        <TaskTable
          title="Pending Tasks"
          tasks={pendingTasks}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onComplete={handleComplete}
          onUndo={handleUndo}
        />
      </div>

      <div>
        <h2 className="text-2xl font-semibold mb-4">Completed Tasks</h2>
        <TaskTable
          title="Completed Tasks"
          tasks={completedTasks}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onComplete={handleComplete}
          onUndo={handleUndo}
        />
      </div>

      {/* Show the form only when a task is selected (for editing) */}
      {selectedTask && (
        <TaskForm task={selectedTask} onSave={handleSave} onClose={() => setSelectedTask(null)} />
      )}
    </div>
  );
}

