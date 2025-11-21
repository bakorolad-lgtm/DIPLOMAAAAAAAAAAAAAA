import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getCourse } from "../api";

export default function CoursePage() {
const { id } = useParams();
const [course, setCourse] = useState(null);
const [loading, setLoading] = useState(true);
const [previewImage, setPreviewImage] = useState(null); // Для модалки

useEffect(() => {
async function load() {
const course = await getCourse(id);
setCourse(course);
setLoading(false);
}
load();
}, [id]);

if (loading) return <p>Загрузка...</p>;
if (!course) return <p>Курс не найден</p>;

return ( <div> <h2>{course.title}</h2> <p>Автор: {course.author.email}</p>

  <h3>Содержимое</h3>  
  {course.blocks && course.blocks.length > 0 ? (  
    course.blocks.map((block, index) => (  
      <div key={index} style={{ margin: "20px 0" }}>  
        {block.text && <p>{block.text}</p>}  

        {block.file_url && (  
          block.file_url.match(/\.(jpg|jpeg|png|gif)$/i) ? (  
            <img  
              src={block.file_url}  
              alt=""  
              style={{ width: "400px", height: "300px", objectFit: "cover", borderRadius: 8, cursor: "pointer" }}  
              onClick={() => setPreviewImage(block.file_url)} // открытие картинки  
            />  
          ) : block.file_url.match(/\.(mp4|webm|mov)$/i) ? (  
            <video controls style={{ width: "400px", height: "300px", objectFit: "cover", borderRadius: 8 }}>  
              <source src={block.file_url} />  
            </video>  
          ) : (  
            <a href={block.file_url} target="_blank" rel="noreferrer">  
              Скачать файл  
            </a>  
          )  
        )}  
      </div>  
    ))  
  ) : (  
    <p>Нет блоков</p>  
  )}  

  {/* Модальное окно для картинки */}  
  {previewImage && (  
    <div  
      onClick={() => setPreviewImage(null)}  
      style={{  
        position: "fixed",  
        top: 0,  
        left: 0,  
        width: "100%",  
        height: "100%",  
        backgroundColor: "rgba(0,0,0,0.8)",  
        display: "flex",  
        justifyContent: "center",  
        alignItems: "center",  
        zIndex: 1000,  
        cursor: "pointer"  
      }}  
    >  
      <img src={previewImage} alt="" style={{ maxWidth: "90%", maxHeight: "90%", borderRadius: 8 }} />  
    </div>  
  )}  
</div>  
);
}
