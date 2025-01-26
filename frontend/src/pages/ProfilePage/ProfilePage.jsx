import { useParams } from "react-router";

export default function ProfilePage() {
  const { userId } = useParams();

  return (
    <div className="mt-32 p-4 bg-purple-200">
      <h1 className="text-2xl font-bold">User Profile</h1>
      <p>User ID: {userId}</p>
    </div>
  );
}
