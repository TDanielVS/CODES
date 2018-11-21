using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class VelocidadTxt : MonoBehaviour {

    public Text texto;
    public Rigidbody m_Rigidbody;
    private float speed;
    private string cad;
    // Use this for initialization
    void Start () {
        texto.text = "0";
        m_Rigidbody = GetComponent<Rigidbody>();
        speed = m_Rigidbody.velocity.magnitude;

    }
	
	// Update is called once per frame
	void Update () {
        speed = m_Rigidbody.velocity.magnitude;
        speed *= .36f;

        if (speed < 0.001)
            speed = 0;

        cad = speed.ToString();
        if(cad.Length > 5)
        {
            cad = cad.Substring(0, 4);
        }

        texto.text = cad + "Km/h";

    }
}
