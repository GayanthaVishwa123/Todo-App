'use client'; // Marking this as a client-side component

import React, { useState } from 'react';

type Todo = {
  id: number;
  title: string;
  deadline: string;
  priority: 'Low' | 'Medium' | 'High';
  comments: string;
  completed: boolean;
};

const TodoApp = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [open, setOpen] = useState(false); // Modal visibility
  const [editing, setEditing] = useState<Todo | null>(null); // For editing tasks

  const [title, setTitle] = useState('');
  const [deadline, setDeadline] = useState('');
  const [priority, setPriority] = useState<'Low' | 'Medium' | 'High'>('Medium');
  const [comments, setComments] = useState('');

  // Reset form
  const resetForm = () => {
    setTitle('');
    setDeadline('');
    setPriority('Medium');
    setComments('');
    setEditing(null);
    setOpen(false);
  };

  // Save new or update task
  const saveTask = () => {
    if (!title) return alert('Title is required');

    if (editing) {
      // Update existing task
      setTodos(todos.map(t =>
        t.id === editing.id
          ? { ...editing, title, deadline, priority, comments }
          : t
      ));
    } else {
      // Add new task
      setTodos([
        ...todos,
        {
          id: Date.now(),
          title,
          deadline,
          priority,
          comments,
          completed: false
        }
      ]);
    }
    resetForm();
  };

  // Edit task
  const editTask = (task: Todo) => {
    setEditing(task);
    setTitle(task.title);
    setDeadline(task.deadline);
    setPriority(task.priority);
    setComments(task.comments);
    setOpen(true);
  };

  // Mark task as completed
  const completeTask = (id: number) => {
    setTodos(todos.map(t => t.id === id ? { ...t, completed: true } : t));
  };

  // Delete task
  const deleteTask = (id: number) => {
    setTodos(todos.filter(t => t.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-50 p-10">
      <div className="max-w-7xl mx-auto bg-white rounded-xl shadow-xl p-8">
        {/* HEADER */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-extrabold text-gray-800">📋 Task Manager</h1>
          <button
            onClick={() => setOpen(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition-all"
          >
            + Add Task
          </button>
        </div>

        {/* ACTIVE TASKS TABLE */}
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Active Tasks</h2>
        <table className="w-full text-left border-collapse mb-8">
          <thead>
            <tr className="border-b bg-gray-100 text-gray-600">
              <th className="py-3 px-6">Title</th>
              <th className="py-3 px-6">Deadline</th>
              <th className="py-3 px-6">Priority</th>
              <th className="py-3 px-6">Status</th>
              <th className="py-3 px-6 text-right">Actions</th>
            </tr>
          </thead>

          <tbody>
            {todos.filter(task => !task.completed).map(task => (
              <tr key={task.id} className="border-b hover:bg-gray-50">
                <td className="py-3 px-6 font-medium">{task.title}</td>
                <td className="py-3 px-6">{task.deadline || '-'}</td>
                <td className="py-3 px-6">
                  <span className={`px-3 py-1 rounded-full text-sm
                    ${task.priority === 'High' && 'bg-red-100 text-red-800'}
                    ${task.priority === 'Medium' && 'bg-yellow-100 text-yellow-800'}
                    ${task.priority === 'Low' && 'bg-green-100 text-green-800'}
                  `}>
                    {task.priority}
                  </span>
                </td>
                <td className="py-3 px-6">
                  {task.completed
                    ? <span className="text-green-600">Completed</span>
                    : <span className="text-gray-500">Active</span>}
                </td>
                <td className="py-3 px-6 text-right space-x-4">
                  {!task.completed && (
                    <button
                      onClick={() => completeTask(task.id)}
                      className="text-green-600 hover:underline transition-all"
                    >
                      Complete
                    </button>
                  )}
                  <button
                    onClick={() => editTask(task)}
                    className="text-blue-600 hover:underline transition-all"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="text-red-600 hover:underline transition-all"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* COMPLETED TASKS TABLE */}
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Completed Tasks</h2>
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b bg-gray-100 text-gray-600">
              <th className="py-3 px-6">Title</th>
              <th className="py-3 px-6">Deadline</th>
              <th className="py-3 px-6">Priority</th>
              <th className="py-3 px-6">Status</th>
              <th className="py-3 px-6 text-right">Actions</th>
            </tr>
          </thead>

          <tbody>
            {todos.filter(task => task.completed).map(task => (
              <tr key={task.id} className="border-b hover:bg-gray-50">
                <td className="py-3 px-6 font-medium">{task.title}</td>
                <td className="py-3 px-6">{task.deadline || '-'}</td>
                <td className="py-3 px-6">
                  <span className={`px-3 py-1 rounded-full text-sm
                    ${task.priority === 'High' && 'bg-red-100 text-red-800'}
                    ${task.priority === 'Medium' && 'bg-yellow-100 text-yellow-800'}
                    ${task.priority === 'Low' && 'bg-green-100 text-green-800'}
                  `}>
                    {task.priority}
                  </span>
                </td>
                <td className="py-3 px-6">
                  {task.completed
                    ? <span className="text-green-600">Completed</span>
                    : <span className="text-gray-500">Active</span>}
                </td>
                <td className="py-3 px-6 text-right space-x-4">
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="text-red-600 hover:underline transition-all"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* SIDE PANEL (TASK DETAILS) */}
      {open && (
        <div className="fixed inset-0 bg-black/50 flex justify-end">
          <div className="w-[420px] bg-white h-full p-6 shadow-xl transform transition-all">

            <h2 className="text-2xl font-semibold mb-4 text-gray-800">
              {editing ? 'Update Task' : 'Task Details'}
            </h2>

            <div className="space-y-4">
              <input
                className="w-full border px-4 py-2 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Title"
                value={title}
                onChange={e => setTitle(e.target.value)}
              />

              <input
                type="date"
                className="w-full border px-4 py-2 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={deadline}
                onChange={e => setDeadline(e.target.value)}
              />

              <select
                className="w-full border px-4 py-2 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={priority}
                onChange={e => setPriority(e.target.value as any)}
              >
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
              </select>

              <textarea
                className="w-full border px-4 py-2 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Comments"
                rows={4}
                value={comments}
                onChange={e => setComments(e.target.value)}
              />
            </div>

            <div className="flex justify-end gap-4 mt-6">
              <button
                onClick={resetForm}
                className="px-4 py-2 rounded border border-gray-300 text-gray-600 hover:bg-gray-100 transition-all"
              >
                Close
              </button>
              <button
                onClick={saveTask}
                className="px-4 py-2 rounded bg-blue-600 text-white shadow hover:bg-blue-700 transition-all"
              >
                {editing ? 'Update' : 'Save'}
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
};

export default TodoApp;
