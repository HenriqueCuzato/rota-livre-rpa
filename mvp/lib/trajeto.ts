import type { Occurrence } from './data';

export type Point = [number, number];
export const radiusMeters = 25;

function distanceFromSegment(report: Occurrence, start: Point, end: Point) {
  const metersPerDegree = 111195;
  const longitudeScale = metersPerDegree * Math.cos(report.lat * Math.PI / 180);
  const ax = (start[1] - report.lng) * longitudeScale;
  const ay = (start[0] - report.lat) * metersPerDegree;
  const dx = (end[1] - start[1]) * longitudeScale;
  const dy = (end[0] - start[0]) * metersPerDegree;
  const lengthSquared = dx * dx + dy * dy;
  const fraction = lengthSquared ? Math.max(0, Math.min(1, -(ax * dx + ay * dy) / lengthSquared)) : 0;
  return Math.hypot(ax + fraction * dx, ay + fraction * dy);
}

export function nearbyReports(rows: Occurrence[], path: Point[]) {
  if (path.length < 2) return [];
  return rows.filter(row => row.status !== 'Resolvida').map(row => {
    let distance = Infinity;
    for (let i = 1; i < path.length; i++) {
      distance = Math.min(distance, distanceFromSegment(row, path[i - 1], path[i]));
    }
    return {row, distance};
  }).filter(alert => alert.distance <= radiusMeters).sort((a, b) => a.distance - b.distance);
}
