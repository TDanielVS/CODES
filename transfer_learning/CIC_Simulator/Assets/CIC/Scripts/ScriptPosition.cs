using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ScriptPosition : MonoBehaviour {

    private static ScriptPosition thisClass;
    private string def;
    private Scene actualScene;
    private bool moved;
    private string pos;
    // Use this for initialization
    void Awake()
    {
        //RD: 45,10.7,0,-15.6
        //RI: 45,8.1,0,-13
        //FD: 225,18,0,-3.1
        //FI: 225,20.6,0,-5.7
        //def = ("225,18,0,-3.1");
        pos = "FD";
        moved = false;
        if (thisClass == null)
        {
            thisClass = this;
            DontDestroyOnLoad(thisClass);
        }
        else Destroy(this);

    }

    public void Update()
    {
        if (Input.GetKey(KeyCode.Escape) && SceneManager.GetActiveScene().name == "MenuScene")
        {
            Application.Quit();
        }
    }

    public void SetPosition(string datos)
    {
        pos = datos;
    }

    public void MoveCar()
    {
        GameObject carro = null;
        string[] data = def.Split(',');
        moved = true;
        actualScene = SceneManager.GetActiveScene();

        if (actualScene.name == "CICTrackTraining")
        {
            carro = GameObject.Find("CarTraining");
        }
        else if(actualScene.name == "CICTrackAutonomous")
        {
            carro = GameObject.Find("CarAutonomous");
        }
        
        carro.GetComponent<Transform>().position = new Vector3(float.Parse(data[1]), float.Parse(data[2]), float.Parse(data[3]));
        carro.GetComponent<Transform>().Rotate(0f, float.Parse(data[0]), 0f);
    }

    public void SetCarPos()
    {
        GameObject carro = null;
        GameObject target = null;
        moved = true;
        actualScene = SceneManager.GetActiveScene();

        if (actualScene.name == "CICTrackTraining" || actualScene.name == "CICTrackTraining2")
        {
            carro = GameObject.Find("CarTraining");
        }
        else if (actualScene.name == "CICTrackAutonomous" || actualScene.name == "CICTrackAutonomous2")
        {
            carro = GameObject.Find("CarAutonomous");
        }

        //Busca la posición de la referencia seleccionada: FD, FI, RD, RI

        target = GameObject.Find(pos);
        carro.GetComponent<Transform>().position = target.GetComponent<Transform>().position;
        carro.GetComponent<Transform>().rotation = target.transform.localRotation;


    }

}
