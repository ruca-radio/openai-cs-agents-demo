"use client";

import { PanelSection } from "./panel-section";
import { Card, CardContent } from "@/components/ui/card";
import { BookText } from "lucide-react";

interface ConversationContextProps {
  context: {
    user_id?: string;
    total_earnings?: number;
    available_skills?: string[];
    min_hourly_rate?: number;
    success_rate?: number;
    current_task?: any;
    active_tasks?: any[];
    completed_tasks?: any[];
  };
}

export function ConversationContext({ context }: ConversationContextProps) {
  return (
    <PanelSection
      title="Task Context"
      icon={<BookText className="h-4 w-4 text-blue-600" />}
    >
      <Card className="bg-gradient-to-r from-white to-gray-50 border-gray-200 shadow-sm">
        <CardContent className="p-3">
          <div className="grid grid-cols-1 gap-2">
            {Object.entries(context).map(([key, value]) => {
              // Format arrays and objects nicely
              const displayValue = Array.isArray(value) 
                ? value.length > 0 ? `[${value.length} items]` : "[]"
                : typeof value === 'object' 
                ? value ? JSON.stringify(value, null, 2) : "null"
                : value?.toString() || "null";
              
              return (
                <div
                  key={key}
                  className="flex items-center gap-2 bg-white p-2 rounded-md border border-gray-200 shadow-sm transition-all"
                >
                  <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                  <div className="text-xs flex-1">
                    <span className="text-zinc-500 font-light">{key.replace(/_/g, ' ')}:</span>{" "}
                    <span
                      className={
                        value
                          ? "text-zinc-900 font-light"
                          : "text-gray-400 italic"
                      }
                    >
                      {displayValue}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </PanelSection>
  );
}