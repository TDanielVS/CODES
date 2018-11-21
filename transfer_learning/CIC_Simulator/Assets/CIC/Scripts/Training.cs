using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System;

public class Training : MonoBehaviour {

    [Range(0, 5)]
    public float tiempo = 1;
    public int frame_rate = 60;
    public Text texto;
    public Boolean grabar = false;
    [Range(1, 10)]
    public int cadaNFrames = 1;

    private string path;
    private int cnt_frames;
    private ArrayList steer;
    private int img_cont;
    private StreamWriter writer;
    

    //private float angulo;
    // Use this for initialization
    void Start () {
        QualitySettings.vSyncCount = 0;
        Time.timeScale = tiempo;
        Application.targetFrameRate = frame_rate;
        cnt_frames = 0;
        img_cont = 0;
        path = Application.dataPath;

        path = "Assets/Datos";
        if (grabar){
            if (Directory.Exists(path))
            {
                Debug.Log("Folder");
                Directory.Delete(path, true);
                Directory.CreateDirectory(path);
                Directory.CreateDirectory(path + "/Images");
            }
            else
            {
                Directory.CreateDirectory(path);
                Directory.CreateDirectory(path + "/Images");
            }

            writer = new StreamWriter(path + "/datos.txt", true, System.Text.Encoding.UTF8);
            writer.WriteLine("Imagen, angulo");
            StartCoroutine(EndFrame());
        }
    }
	
    /*void FixedUpdate()
    {

        //if (cnt_frames > 8 && cnt_frames % 2 == 0)
        if (grabar){
            if (cnt_frames > 8){
                //Capture
                cnt_frames = -1;
                float angulo = Input.GetAxis("Horizontal");

                Debug.Log("Ang:" + angulo.ToString());
                name = string.Format("{0}{1}.png", DateTime.Now.ToString("yyy_MM_dd_HH-mm_"), img_cont.ToString("000000"));

                Debug.Log(path + "/Images/" + name);
                ScreenCapture.CaptureScreenshot(path + "/Images/" + name);
                writer.WriteLine(name + ", " + angulo.ToString());

                img_cont++;
            }

            cnt_frames++;
        }
    }*/

    

	// Update is called once per frame
	void Update () {
        //Debug.Log("Fr: " + Application.targetFrameRate);
        if (Application.targetFrameRate != frame_rate){
            Application.targetFrameRate = frame_rate;
        }
        if (grabar)
        {
            texto.enabled = false;
        }
        else
        {
            texto.enabled = true;
        }
    }

    void OnApplicationQuit()
    {
        if (grabar){
            writer.Close();
        }
        Debug.Log("Application ending after " + Time.time + " seconds");
    }


    IEnumerator EndFrame()
    {
        while (Application.isPlaying)
        {
            yield return new WaitForEndOfFrame();
            if (cnt_frames % cadaNFrames == 0) { 
                float angulo = Input.GetAxis("Horizontal");
                name = string.Format("{0}{1}.png", DateTime.Now.ToString("yyy_MM_dd_HH-mm_"), img_cont.ToString("000000"));
                ScreenCapture.CaptureScreenshot(path + "/Images/" + name);
                writer.WriteLine(name + ", " + angulo.ToString());
                img_cont++;
            }
            cnt_frames++;
        }
    }



}
