using System.Collections;
using System.Collections.Generic;
using System;
using System.IO;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class HandPointer : MonoBehaviour {

    public int currentCursorIndex = 0;
    public Text TimeScale;
    public Text CurrentHandIndex;

    public bool isDown = false;

    public int oldScreenWidth;
    public int oldScreenHeight;
    
    CursorMode cursorMode = CursorMode.Auto;
    Vector2 hotSpot = Vector2.zero;

    [SerializeField]
    public List<Texture2D> MouseUpPointer = new List<Texture2D>();

    [SerializeField]
    public List<Texture2D> MouseDownPointer = new List<Texture2D>();

    public static Texture2D ResizeTexture(Texture2D pSource, float wScale, float hScale) {

        //*** Variables

        //*** Get All the source pixels
        Color[] aSourceColor = pSource.GetPixels(0);
        Vector2 vSourceSize = new Vector2(pSource.width, pSource.height);

        Debug.Log("pSource width : " + pSource.width + "  pSource.height : " + pSource.height);
        Debug.Log("wScale : " + wScale + " hScale : " + hScale);
        //*** Calculate New Size
        float xWidth = Mathf.RoundToInt((float)pSource.width * wScale);                     
        float xHeight = Mathf.RoundToInt((float)pSource.height * hScale);

        Debug.Log("xWidth : " + xWidth + "  xHeight : " + xHeight);
        //*** Make New
        Texture2D oNewTex = new Texture2D((int)xWidth, (int)xHeight, TextureFormat.ARGB32, false);

        //*** Make destination array
        int xLength = (int)xWidth * (int)xHeight;
        Color[] aColor = new Color[xLength];
        
        Vector2 vPixelSize = new Vector2(vSourceSize.x / xWidth, vSourceSize.y / xHeight);

        //*** Loop through destination pixels and process
        Vector2 vCenter = new Vector2();
        for(int i = 0; i<xLength; i++) {

            //*** Figure out x&y
            float xX = (float)i % xWidth;
            float xY = Mathf.Floor((float)i / xWidth);

            //*** Calculate Center
            vCenter.x = (xX / xWidth) * vSourceSize.x;
            vCenter.y = (xY / xHeight) * vSourceSize.y;

            //*** Bilinear
            //*** Get Ratios
            float xRatioX = vCenter.x - Mathf.Floor(vCenter.x);
            float xRatioY = vCenter.y - Mathf.Floor(vCenter.y);

            //*** Get Pixel index's
            int xIndexTL = (int)((Mathf.Floor(vCenter.y) * vSourceSize.x) + Mathf.Floor(vCenter.x));
            int xIndexTR = (int)((Mathf.Floor(vCenter.y) * vSourceSize.x) + Mathf.Ceil(vCenter.x));
            int xIndexBL = (int)((Mathf.Ceil(vCenter.y) * vSourceSize.x) + Mathf.Floor(vCenter.x));
            int xIndexBR = (int)((Mathf.Ceil(vCenter.y) * vSourceSize.x) + Mathf.Ceil(vCenter.x));

            if( xIndexTL >= aSourceColor.Length) xIndexTL = aSourceColor.Length-1;
            if( xIndexTR >= aSourceColor.Length) xIndexTR = aSourceColor.Length-1;
            if( xIndexBL >= aSourceColor.Length) xIndexBL = aSourceColor.Length-1;
            if( xIndexBR >= aSourceColor.Length) xIndexBR = aSourceColor.Length-1;

            try {
            //*** Calculate Color
            aColor[i] = Color.Lerp(
                    Color.Lerp(aSourceColor[xIndexTL], aSourceColor[xIndexTR], xRatioX),
                    Color.Lerp(aSourceColor[xIndexBL], aSourceColor[xIndexBR], xRatioX),
                    xRatioY
                    );
            }
            catch (IndexOutOfRangeException e) {
                Debug.Log("aSourceColor : " + aSourceColor.Length);
                Debug.Log("xIndexTL : " + xIndexTL);
                Debug.Log("xIndexTR : " + xIndexTR);
                Debug.Log("xIndexBL : " + xIndexBL);
                Debug.Log("xIndexBR : " + xIndexBR);
                Debug.Log("xRatioX : " + xRatioX);
                Debug.Log("xRatioY : " + xRatioY);
                Debug.Log("aSourceColor[xIndexTL] : " + aSourceColor[xIndexTL]);
                Debug.Log("aSourceColor[xIndexTR] : " + aSourceColor[xIndexTR]);
                Debug.Log("aSourceColor[xIndexBL]: " + aSourceColor[xIndexBL]);
                Debug.Log("aSourceColor[xIndexBR]: " + aSourceColor[xIndexBR]);
            }
        }

        //*** Set Pixels
        oNewTex.SetPixels(aColor);
        oNewTex.Apply();

        //*** Return
        return oNewTex;
    }

    public static void Init() {
        GameObject prefab = Resources.Load("HandPointer", typeof(GameObject)) as GameObject;
        GameObject go = Instantiate(prefab) as GameObject;
    }

    void Awake() {
        DontDestroyOnLoad(this);

        string filePath = Application.dataPath+"/Data/HandTextures/";
        for (int i = 0; i < 10; ++i) {
            if (File.Exists(filePath+(i+1)+"_1.png") && File.Exists(filePath+(i+1)+"_2.png")) {
                Debug.Log("Find!");
                byte[] fileData;               
                fileData = File.ReadAllBytes(filePath+(i+1)+"_1.png");
                Texture2D tex1 = new Texture2D(2, 2);
                tex1.LoadImage(fileData);
                MouseUpPointer.Add(tex1);
                
                fileData = File.ReadAllBytes(filePath+(i+1)+"_2.png");
                Texture2D tex2 = new Texture2D(2, 2);
                tex2.LoadImage(fileData);
                MouseDownPointer.Add(tex2);
            }
        }
    }

    // Use this for initialization
    void Start () {
        TimeScale.text = Time.timeScale.ToString();
        CurrentHandIndex.text = currentCursorIndex.ToString();
    }

    // Update is called once per frame
    void Update () {

        foreach (char c in Input.inputString) {
            if (Char.IsNumber(c)) {
               var val = (int)Char.GetNumericValue(c);
               if (currentCursorIndex != val && (val < MouseUpPointer.Count)) {
                   currentCursorIndex = val;
                   CurrentHandIndex.text = String.Format("Changed {0}th hand image.", currentCursorIndex);
                   StopCoroutine("IndexTextEffect");
                   StartCoroutine("IndexTextEffect");
               }
            }
        }

        if (Input.GetKeyUp(KeyCode.UpArrow)) {
            Time.timeScale += 0.1f;
            Time.fixedDeltaTime = 0.02f * Time.timeScale;
            TimeScale.text = "TimeScale : " + (Mathf.Round(Time.timeScale * 100.0f)/100f).ToString();
            StopCoroutine("TimeScaleTextEffect");
            StartCoroutine("TimeScaleTextEffect");
        } else if (Input.GetKeyUp(KeyCode.DownArrow)) {
            if (Time.timeScale > 0.1) {
                Time.timeScale -= 0.1f;
                Time.fixedDeltaTime = 0.02f * Time.timeScale;
                TimeScale.text = "TimeScale : " + (Mathf.Round(Time.timeScale * 100.0f)/100f).ToString();
                StopCoroutine("TimeScaleTextEffect");
                StartCoroutine("TimeScaleTextEffect");
            }

        } 

        if (Input.GetMouseButton(0)) {
            isDown = true;
        } else {
            isDown = false;
        }
        if (!isDown){
            hotSpot = new Vector2(MouseUpPointer[currentCursorIndex].width/5*2 , MouseUpPointer[currentCursorIndex].height*0.03f);
            Cursor.SetCursor(MouseUpPointer[currentCursorIndex], hotSpot, cursorMode);
        } else {
            hotSpot = new Vector2(MouseUpPointer[currentCursorIndex].width/5*2 , MouseUpPointer[currentCursorIndex].height*0.03f);
            Cursor.SetCursor(MouseDownPointer[currentCursorIndex], hotSpot, cursorMode);
        }
    }

    IEnumerator TimeScaleTextEffect() {
        TimeScale.color = new Color(TimeScale.color.r, TimeScale.color.g, TimeScale.color.b, 1);
        while (TimeScale.color.a > 0.0f) {
            TimeScale.color = new Color(TimeScale.color.r, TimeScale.color.g, TimeScale.color.b, TimeScale.color.a - (Time.deltaTime/1f));
            yield return null;
        }
    }

    IEnumerator IndexTextEffect() {
        CurrentHandIndex.color = new Color(CurrentHandIndex.color.r, CurrentHandIndex.color.g, CurrentHandIndex.color.b, 1);
        while (TimeScale.color.a > 0.0f) {
            CurrentHandIndex.color = new Color(CurrentHandIndex.color.r, CurrentHandIndex.color.g, CurrentHandIndex.color.b, CurrentHandIndex.color.a - (Time.deltaTime/1f));
            yield return null;
        }

    }

}
