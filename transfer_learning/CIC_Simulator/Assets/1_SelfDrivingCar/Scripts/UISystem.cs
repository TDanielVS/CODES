using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using UnityStandardAssets.Vehicles.Car;
using UnityEngine.SceneManagement;

public class UISystem : MonoSingleton<UISystem> {

    public CarController carController;
    public string GoodCarStatusMessage;
    public string BadSCartatusMessage;
    public Text MPH_Text;
    public Image MPH_Animation;
    public Text Angle_Text;
    public Text RecordStatus_Text;
	public Text DriveStatus_Text;
	public Text SaveStatus_Text;
    public GameObject RecordingPause; 
	public GameObject RecordDisabled;
	public bool isTraining = false;
    public GameObject panelLuces;
    public Camera editCamera;
    public GameObject ambientLight;

    private bool recording;
    private float topSpeed;
	private bool saveRecording;
    private GameObject a1ref, a2ref, a4ref;

    // Use this for initialization
    void Start() {
        a1ref = GameObject.Find("A1");
        a2ref = GameObject.Find("A2");
        a4ref = GameObject.Find("A4");
		Debug.Log (isTraining);
        editCamera.enabled = false;
        topSpeed = carController.MaxSpeed;
        recording = false;
        RecordingPause.SetActive(false);
		RecordStatus_Text.text = "RECORD";
		DriveStatus_Text.text = "";
		SaveStatus_Text.text = "";
		SetAngleValue(0);
        SetMPHValue(0);
		if (!isTraining) {
			DriveStatus_Text.text = "Mode: Autonomous";
			RecordDisabled.SetActive (true);
			RecordStatus_Text.text = "";
		} 
    }

    public void SetAngleValue(float value)
    {
        Angle_Text.text = value.ToString("N2") + "°";
    }

    public void SetMPHValue(float value)
    {
        MPH_Text.text = value.ToString("N2");
        //Do something with value for fill amounts
        MPH_Animation.fillAmount = value/topSpeed;
    }

    public void ToggleRecording()
    {
		// Don't record in autonomous mode
		if (!isTraining) {
			return;
		}

        panelLuces.SetActive(false);
        editCamera.enabled = false;
        if (!recording)
        {
            if (carController.checkSaveLocation()) 
			{
				recording = true;
				RecordingPause.SetActive (true);
				RecordStatus_Text.text = "RECORDING";
				carController.IsRecording = true;
			}
        }
        else
        {
			saveRecording = true;
			carController.IsRecording = false;
            
        }
    }
	
    public void EditLights()
    {
        if (!recording)
        {
            //Edit the lights
            if (!panelLuces.activeSelf)
            {
                panelLuces.SetActive(true);
                editCamera.enabled = true;
            }
            else
            {
                panelLuces.SetActive(false);
                editCamera.enabled = false;
            }
        }
    }

    public void Apagador(Button apagador)
    {
        ColorBlock colorActual = apagador.colors;

        if (colorActual.normalColor != Color.red)
        {
            colorActual.normalColor = Color.red;
            colorActual.highlightedColor = Color.red;
        }
        else
        {
            colorActual.normalColor = new Color(0f, 1f, 0.172f);
            colorActual.highlightedColor = new Color(0f, 1f, 0.172f);
        }
        apagador.colors = colorActual;
    }

    public void ActivarLuces(GameObject luces)
    {
        if (luces.activeSelf)
        {
            luces.SetActive(false);
        }
        else
        {
            luces.SetActive(true);
        }
    }



    void UpdateCarValues()
    {
        SetMPHValue(carController.CurrentSpeed);
        SetAngleValue(carController.CurrentSteerAngle);
    }

	// Update is called once per frame
	void Update () {

        // Easier than pressing the actual button :-)
        // Should make recording training data more pleasant.
        if (a1ref.activeSelf && a2ref.activeSelf && a4ref.activeSelf)
        {
            ambientLight.SetActive(true);
        }
        else
        {
            ambientLight.SetActive(false);
        }

		if (carController.getSaveStatus ()) {
			SaveStatus_Text.text = "Capturing Data: " + (int)(100 * carController.getSavePercent ()) + "%";
			//Debug.Log ("save percent is: " + carController.getSavePercent ());
		} 
		else if(saveRecording) 
		{
			SaveStatus_Text.text = "";
			recording = false;
			RecordingPause.SetActive(false);
			RecordStatus_Text.text = "RECORD";
			saveRecording = false;
		}

        if (Input.GetKeyDown(KeyCode.R))
        {
            ToggleRecording();
        }

		if (!isTraining) 
		{
			if ((Input.GetKey(KeyCode.W)) || (Input.GetKey(KeyCode.S))) 
			{
				DriveStatus_Text.color = Color.red;
				DriveStatus_Text.text = "Mode: Manual";
			} 
			else 
			{
				DriveStatus_Text.color = Color.white;
				DriveStatus_Text.text = "Mode: Autonomous";
			}
		}

	    if(Input.GetKeyDown(KeyCode.Escape))
        {
            //Do Menu Here
            SceneManager.LoadScene("MenuScene");
        }

        if (Input.GetKeyDown(KeyCode.Return))
        {
            //Do Console Here
        }

        UpdateCarValues();
    }
}
