using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class MenuOptions : MonoBehaviour
{

    public Sprite track1;
    public Sprite track2;

    private int track = 0;
    private Outline[] outlines;

    public void Start ()
    {
        outlines = GetComponentsInChildren<Outline>();
		Debug.Log ("in menu script "+outlines.Length);
		if (outlines.Length > 0) 
		{
			outlines [0].effectColor = new Color (0, 0, 0);
		}
    }


	public void MainMenu()
	{
		Debug.Log ("go to main menu");
		SceneManager.LoadScene("MenuScene", LoadSceneMode.Single);
	}

    public void StartDrivingMode()
    {
        if (track == 0) {
            SceneManager.LoadScene("CICTrackTraining", LoadSceneMode.Single);
        }
        else
        {
            SceneManager.LoadScene("CICTrackTraining2", LoadSceneMode.Single);
        }

    }

    public void StartAutonomousMode()
    {
        if (track == 0) {
            SceneManager.LoadScene("CICTrackAutonomous", LoadSceneMode.Single);
        }
        else
        {
            SceneManager.LoadScene("CICTrackAutonomous2", LoadSceneMode.Single);
        }
    }

    public void ChangeTrack()
    {
        Image imagen = GameObject.Find("TrackImage").GetComponent<Image>();
        if (track == 0)
        {
            track = 1;
            imagen.sprite = track2;
        }
        else
        {
            track = 0;
            imagen.sprite = track1;
        }
    }

    public void SetCICTrack()
    {
        track = 0;
        outlines[0].effectColor = new Color(0, 0, 0);
    }

}
