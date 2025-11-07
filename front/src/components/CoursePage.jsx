import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getCourse } from "../api";

export default function CoursePage() {
  const { id } = useParams();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log("Course page")
    console.log(id)
    async function load() {
      const course = await getCourse(id);
      setCourse(course);
      setLoading(false);
    }
    load();
  }, [id]);

  if (loading) return <p>Загрузка...</p>;
  if (!course) return <p>Курс не найден</p>;

  return (
    <div>
      <h2>{course.title}</h2>
      <p>{course.description}</p>
      <p>Created by {course.author.email}</p>
    </div>
  );
}