import { useParams } from "react-router";

export default function ReportPage() {
  const { userId, postId } = useParams();

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Report Page</h1>
      <p>User ID: {userId}</p>
      <p>Post ID: {postId}</p>
      {/* Add logic to fetch and display report details here */}
    </div>
  );
}
