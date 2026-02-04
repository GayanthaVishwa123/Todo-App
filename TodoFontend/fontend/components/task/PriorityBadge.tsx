'use client';

import { Priority } from '@/types/task';

const styles: Record<Priority, string> = {
  High: 'bg-red-100 text-red-700 ring-red-300',
  Medium: 'bg-yellow-100 text-yellow-700 ring-yellow-300',
  Low: 'bg-green-100 text-green-700 ring-green-300',
};

export default function PriorityBadge({ priority }: { priority: Priority }) {
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ring-1 ${styles[priority]}`}
    >
      {priority}
    </span>
  );
}
